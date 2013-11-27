import sys
import os
#import urllib.request
import urllib2
import urllib
import socket
from threading import Thread
import PySide
from PySide.QtCore import Signal, Slot, QObject
from PySide.QtGui import QApplication, QMainWindow, QMessageBox, QPixmap, QIcon, QFileDialog
from views.main_ui_pyside import Ui_MainWindow
from PySide.QtCore import Qt
from bs4 import BeautifulSoup
import bs4
import re
import tempfile
import subprocess

timeout = 10
socket.setdefaulttimeout(timeout)

def open_url(url):
    return urllib2.urlopen(url)

def get_file(file_name):
    if getattr(sys, 'frozen', False):
        #The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable),"images")
        print(datadir)
    else:
        #The application is not frozen
        datadir = os.path.join(os.path.dirname(__file__), "images")
        print(os.path.join(datadir, file_name))
    return os.path.join(datadir, file_name)


class AnimeList():
    def __init__(self, url):
        page = open_url(url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        links = soup.find_all("div")
        self.number = 0
        self.animes = {}
        for div in links:
            if div.has_attr('class'):
                if div['class'][0] in 'ddmcc':
                    for child in div.children:
                        if child.name in 'ul':
                            for ul_child in child.children:
                                if ul_child.name:
                                    if ul_child.name in 'ul':
                                        for ul_ul_child in ul_child.children:
                                            # this line takes out the spaces in
                                            # the return list
                                            if re.findall(r'(.\b[^ ]*?)', ul_ul_child.string):
                                                self.number += 1
                                                self.animes[
                                                    ul_ul_child.string] = ul_ul_child.a['href']

    def get_attrs(self):
        return self.number, self.animes


class Episode():
    def __init__(self, name, release_date, link):
        self.name = name
        self.release_date = release_date
        self.link = link

    def get_attrs(self):
        return self.name, self.release_date, self.link


class EpisodeList(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        self.episodes = {}
        self.start()

    def run(self):
        page = open_url(self.url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        links = soup.find_all("div")
        if soup.title.string not in 'Removed':
            for div in links:
                if div.has_attr('class'):
                    if div['class'][0] in 'entry':
                        for child in div.children:
                            if child.name:
                                if child.name in 'ul':
                                    for ul_child in child.children:
                                        if ul_child.name:
                                            if ul_child.name in 'li':
                                                for li_child in ul_child.children:
                                                    if isinstance(li_child, bs4.element.Tag):
                                                        episode_link = li_child[
                                                            'href']
                                                        name = False
                                                        release = False
                                                        for ul_li_child in li_child.children:
                                                            if isinstance(ul_li_child, bs4.element.Tag):
                                                                release_date = ul_li_child.string
                                                                release = True
                                                            else:
                                                                episode_name = ul_li_child
                                                                name = True
                                                            if name and release:
                                                                ep = Episode(
                                                                    episode_name, release_date, episode_link)
                                                                self.episodes[
                                                                    ep.name] = ep
                                                                name = False
                                                                release = False
        else:
            self.episodes['Removed'] = ''

    def get_episodes(self):
        return self.episodes


class DownloadOptions(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        self.download_options = {}
        self.img_link = None
        self.start()

    def run(self):
        page = open_url(self.url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        links = soup.find_all("li", {'class': 'tor'})
        self.img_link = soup.find_all('div', {'class': 'post-info-thumb'})[0].img['src']
        for item in links:
            name = item.string
            link = item.contents[0]['href']
            self.download_options[name] = link

    def get_download_options(self):
        return self.download_options

    def get_img_link(self):
        print(self.img_link)
        return self.img_link


class Comunicate(QObject):
    sig = Signal(str)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.searchEdit.textChanged.connect(self.search_text_changed)
        self.ui.show_button.clicked.connect(self.show_episodes)
        self.ui.searchEdit.returnPressed.connect(self.show_episodes)
        self.episodes = None
        self.episode_list = None
        self.number = 0
        self.anime_list = None
        self.ui.download_button.clicked.connect(self.download)
        self.ui.res_list_widget.currentItemChanged.connect(self.download_item_change)
        self.com = Comunicate()
        self.com.sig.connect(self.message)
        self.ui.anime_list_widget.itemDoubleClicked.connect(self.show_episodes)
        self.setWindowIcon(QIcon(get_file('animes.png')))
        Thread(target=self.load_url_items).start()

    @Slot(str)
    def message(self, message):
        if message in 'ended':
            self.ui.loading_label.setVisible(False)
            self.repaint()
        if message in 'started':
            self.ui.loading_label.setVisible(True)
            self.repaint()

    def load_url_items(self):
        self.com.sig.emit('started')
        self.main_download_page = AnimeList(
            "http://www.animetake.com/anime-downloads/")
        self.number, self.anime_list = self.main_download_page.get_attrs()
        self.ui.avaLabel.setText('%s available.' % self.number)
        self.add_full_items_animelist()
        self.com.sig.emit('ended')

    def download_item_change(self):
        self.com.sig.emit('started')
        self.repaint()
        self.ui.options_list_widget.clear()

        #urllib.request.urlretrieve("http://animetake.com/images/.png", "images" + os.sep + "onepiece.png")
        #pix = QPixmap("images" + os.sep + "onepiece.png")#%s" % str(anime_name).replace(' ', '-'))
        #self.ui.image_label.setPixmap(pix)

        if self.ui.res_list_widget.currentItem():
            name = self.ui.res_list_widget.currentItem().text().split(' -->')[0]
            ep = self.episode_list[name]
            name, release_date, link = ep.get_attrs()
            download = DownloadOptions(link)
            download.join()
            img_link = download.get_img_link()
            file_name = img_link
            if file_name is not None:
                file_name = img_link.replace('http://www.animetake.com/images/', '')
            if os.path.exists(get_file(file_name)):
                self.ui.image_label.setPixmap(get_file(file_name))
            else:
                #urllib.request.urlretrieve('http://www.animetake.com/images/%s' % file_name,
                #                           'images' + os.sep + file_name)
                urllib.urlretrieve('http://www.animetake.com/images/%s' % file_name,get_file(file_name))
                self.ui.image_label.setPixmap(get_file(file_name))
            self.options = download.get_download_options()
            for name, link in self.options.items():
                self.ui.options_list_widget.addItem(name)
            self.com.sig.emit('ended')

    def download(self):
        name = self.ui.options_list_widget.currentItem().text()
        link = self.options[name]
        self.com.sig.emit('started')
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        file_path = os.path.join(dialog.getExistingDirectory(),"%s.torrent" % name.strip())
        #urllib.request.urlretrieve(link, file_path)
        urllib.urlretrieve(link, file_path)
        self.ui.loading_label.setVisible(False)
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Torrent Download')
        msgBox.setText('Downloaded file %s.torrent to %s.' % (name, file_path))
        msgBox.setInformativeText('Do you want to start the download now?')
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.Yes)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            if sys.platform in 'win32':
                os.startfile(file_path)
            else:
                subprocess.Popen(['ktorrent',file_path])
        self.com.sig.emit('ended')

    def keyPressEvent(self, event):
        if isinstance(event, PySide.QtGui.QKeyEvent):
            if event.key() == Qt.Key_Down:
                self.ui.anime_list_widget.setCurrentRow(
                    self.ui.anime_list_widget.currentRow() + 1)
            elif event.key() == Qt.Key_Up:
                self.ui.anime_list_widget.setCurrentRow(
                    self.ui.anime_list_widget.currentRow() - 1)

    def show_episodes(self):
        self.com.sig.emit('started')
        self.ui.res_list_widget.clear()
        anime_name = self.ui.anime_list_widget.currentItem().text()
        link = self.anime_list[anime_name]
        self.episodes = EpisodeList(link)
        self.repaint()
        self.episodes.join()
        self.episode_list = self.episodes.get_episodes()

        if 'Removed' not in self.episode_list.keys():
            for name, episode in reversed(sorted(self.episode_list.items())):
                name, release_date, link = episode.get_attrs()
                self.ui.res_list_widget.addItem(name + ' -->' + release_date)
        else:
            self.ui.res_list_widget.addItem('This anime is not available, sorry.')
        self.com.sig.emit('ended')

    def add_full_items_animelist(self):
        self.ui.anime_list_widget.clear()
        for name, link in sorted(self.anime_list.items()):
            self.ui.anime_list_widget.addItem(name)

    def search_text_changed(self, new_text):
        items = self.ui.anime_list_widget.findItems(new_text, Qt.MatchContains)
        if items:
            self.ui.anime_list_widget.setCurrentItem(items[0])
            self.ui.labelSearch.setText('')
        else:
            self.ui.labelSearch.setText('Not Found!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import sys
import os
import urllib2
import urllib
import socket
from threading import Thread
import PySide
from PySide.QtCore import Signal, Slot, QObject
from PySide.QtGui import QApplication, QMainWindow, QMessageBox, QPixmap, QIcon, QFileDialog, QMovie, QSystemTrayIcon
from views.main_ui_pyside import Ui_MainWindow
from PySide.QtCore import Qt
from bs4 import BeautifulSoup
import bs4
import subprocess

timeout = 10
socket.setdefaulttimeout(timeout)


def open_url(url):
    return urllib2.urlopen(url)


def get_file(file_name):
    if getattr(sys, 'frozen', False):
        #The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), "images")
        #print(datadir)
    else:
        #The application is not frozen
        datadir = os.path.join(os.path.dirname(__file__), "images")
        #print(os.path.join(datadir, file_name))
    return os.path.join(datadir, file_name)


class AnimeList():
    def __init__(self, url):
        page = open_url(url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        links = soup.find_all("td", {'class': 'views-field views-field-title active'})
        self.animes = {}
        self.number = 0
        for td in links:
            if isinstance(td, bs4.element.Tag):
                for a in td.children:
                    if isinstance(a, bs4.element.Tag):
                        anime_link = 'http://www.anbient.net' + a['href']
                        anime_name = a.string
                        self.animes[anime_name] = anime_link
                        self.number += 1

    def get_attrs(self):
        return self.number, self.animes


class Episode():
    def __init__(self, name):
        self.name = name
        self.links = []

    def get_attrs(self):
        return self.name, self.links


class EpisodeList():
    def __init__(self, url):
        #Thread.__init__(self)
        self.url = url
        self.episodes = {}
        self.sinopse = None
        self.run()
        #self.start()

    def run(self):
        page = open_url(self.url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        links = soup.find_all("div", {'class': 'boxmeio'})
        span_sinopse = soup.find_all('span', {'id': 'sinopse'})
        for chil in span_sinopse:
            if isinstance(chil, bs4.element.Tag):
                self.sinopse = chil.string

        for div in links:
            if isinstance(div, bs4.element.Tag):
                episode_name = div.string
                episode_link = div.parent['href']
                if episode_name not in self.episodes.keys():
                    episode = Episode(episode_name)
                    self.episodes[episode_name] = episode
                    self.episodes[episode_name].links.append(episode_link)
                else:
                    self.episodes[episode_name].links.append(episode_link)

    def get_episodes(self):
        return self.episodes

    def get_sinopse(self):
        return self.sinopse


class Comunicate(QObject):
    sig = Signal(str)
    img = Signal(str)

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
        self.ui.res_list_widget.currentItemChanged.connect(self.episode_change)
        self.com = Comunicate()
        self.com.sig.connect(self.message)
        self.com.img.connect(self.set_image)
        self.ui.anime_list_widget.itemDoubleClicked.connect(self.show_episodes)
        self.setWindowIcon(QIcon(get_file('animes.png')))
        self.ui.anime_list_widget.itemPressed.connect(self.anime_entered)
        Thread(target=self.load_url_items).start()
        self.movie = QMovie(get_file('ajax-loader.gif'))
        self.ui.loading_label.setMovie(self.movie)
        self.link = None
        self.main_download_page = None
        tray = QSystemTrayIcon()
        tray.setIcon(QIcon(get_file('animes.png')))
        tray.show()
        tray.showMessage('MSG', 'Mensaaaaaaagem', msecs=1000)

    @Slot(str)
    def set_image(self, img_str):
        self.ui.image_label.setPixmap(QPixmap(img_str))

    @Slot(str)
    def message(self, message):
        if message in 'ended':
            self.ui.loading_label.hide()
            #self.repaint()
            self.ui.anime_list_widget.setEnabled(True)
            self.ui.show_button.setEnabled(True)
            self.movie.stop()
            pass
        if message in 'started':
            self.ui.loading_label.show()
            #self.repaint()
            self.ui.anime_list_widget.setEnabled(False)
            self.ui.show_button.setEnabled(False)
            self.movie.start()
            pass

    def anime_entered(self, item):
        pass

    def load_url_items(self):
        self.com.sig.emit('started')
        self.main_download_page = AnimeList('http://www.anbient.net/lista')
        self.number, self.anime_list = self.main_download_page.get_attrs()
        self.ui.avaLabel.setText('%s disponiveis.' % self.number)
        self.add_full_items_animelist()
        self.com.sig.emit('ended')

    def episode_change(self):
        self.com.sig.emit('started')
        self.ui.options_list_widget.clear()

        if self.ui.res_list_widget.currentItem():
            name = self.ui.res_list_widget.currentItem().text()
            episode = self.episode_list[name]
            self.ui.options_list_widget.addItems(episode.links)
            self.com.sig.emit('ended')

    def download(self):
        #name = self.ui.options_list_widget.currentItem().text()
        link = self.ui.options_list_widget.currentItem.text()
        self.com.sig.emit('started')
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        file_path = os.path.join(dialog.getExistingDirectory(), "%s.torrent" % name.strip())
        urllib.urlretrieve(link, file_path)
        self.ui.loading_label.hide()
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
                subprocess.Popen(['ktorrent', file_path])
        self.com.sig.emit('ended')

    def keyPressEvent(self, event):
        if isinstance(event, PySide.QtGui.QKeyEvent):
            if event.key() == Qt.Key_Down:
                self.ui.anime_list_widget.setCurrentRow(
                    self.ui.anime_list_widget.currentRow() + 1)
            elif event.key() == Qt.Key_Up:
                self.ui.anime_list_widget.setCurrentRow(
                    self.ui.anime_list_widget.currentRow() - 1)

    @staticmethod
    def get_img_link(url):
        page = urllib2.urlopen(url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        spans = soup.find_all('span', {'id': 'posterspan'})
        link = None
        for chil in spans:
            if isinstance(chil, bs4.element.Tag):
                for img in chil.children:
                    if isinstance(img, bs4.element.Tag):
                        link = img['src']
        return link

    def show_ep_thread(self):
        self.ui.res_list_widget.clear()
        anime_name = self.ui.anime_list_widget.currentItem().text()
        link = self.anime_list[anime_name]
        self.episodes = EpisodeList(link)
        #self.episodes.join()
        self.link = self.get_img_link(link)
        self.episode_list = self.episodes.get_episodes()

        anime_name = self.ui.anime_list_widget.currentItem().text()
        link = self.anime_list[anime_name]
        img_link = self.get_img_link(link)
        file_name = img_link
        if os.path.exists(get_file(file_name)):
            self.com.img.emit(get_file(file_name))
            #self.ui.image_label.setPixmap(QPixmap(get_file(file_name)))
        else:
            if img_link is not None:
                file_name = img_link.replace('http://www.anbient.net/sites/default/files/imagecache/242x0/imagens/poster/', '')
                urllib.urlretrieve(
                    'http://www.anbient.net/sites/default/files/imagecache/242x0/imagens/poster/%s' % file_name,
                    get_file(file_name))
                self.com.img.emit(get_file(file_name))
                #self.ui.image_label.setPixmap(QPixmap(get_file(file_name)))

        self.ui.label_sinopse.setText(self.episodes.get_sinopse().strip())

        for name, episode in reversed(sorted(self.episode_list.items())):
            name, links = episode.get_attrs()
            self.ui.res_list_widget.addItem(name)
        self.com.sig.emit('ended')

    def show_episodes(self):
        Thread(target=self.show_ep_thread).start()
        self.com.sig.emit('started')

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

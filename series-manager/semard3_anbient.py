#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import subprocess
import sys
import os
import urllib.request, urllib.error, urllib.parse
from urllib.request import Request
import urllib.request, urllib.parse, urllib.error
import urllib.parse
import socket
from threading import Thread
import platform
import webbrowser
from email.mime.text import MIMEText
import smtplib
import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, QObject, QDir, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QSystemTrayIcon, QMenu, \
    QDialog, QFileDialog, QInputDialog, QLineEdit, QProgressBar
from PyQt5.QtCore import Qt, QUrl
from bs4 import BeautifulSoup
import bs4
import pycurl
from views.main_ui_pyqt5 import Ui_MainWindow
from views.feedback_ui_pyqt5 import Ui_FeedbackDialog
from views.browser_ui_pyqt5 import Ui_BrowserWidget
#import vlc

__version__ = '1.0.0'

timeout = 10
socket.setdefaulttimeout(timeout)


def open_url(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req)


def get_file(file_name):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), "images")
        # print(datadir)
    else:
        # The application is not frozen
        datadir = os.path.join(os.path.dirname(__file__), "images")
        #print(os.path.join(datadir, file_name))
    return os.path.join(datadir, file_name)


@Slot(str)
def m_box_exec(message):
    """Show message box (error)
    @param message: message to show on QMessageBox"""
    QMessageBox.critical(None, 'Error!', message, QMessageBox.Ok)


@Slot(str)
def m_box_exec_success(message):
    """Show message box (sucess)
    @param message: message to show on QMessageBox"""
    QMessageBox.information(None, 'Sucess!', message, QMessageBox.Ok)


class Comunicate(QObject):
    sig = Signal(str)
    img = Signal(str)
    op = Signal(str)
    msg = Signal(str)
    mBox = Signal(str)
    mBoxEr = Signal(str)


class EmailSender(Thread):
    """Sends feedback mail"""

    def __init__(self, nome, app_name, email, mensagem, com):
        Thread.__init__(self)
        self.mensagem = mensagem
        self.app_name = app_name
        self.email = email
        self.nome = nome
        self.com = com

    def run(self):
        """Calls self.send_mail()"""
        self.send_mail(self.nome, self.app_name, self.email, self.mensagem)

    def send_mail(self, nome, app_name, email, mensagem):
        """Sends the email to suporte@roandigital"""
        try:
            sender = "contato@roandigFile nameital.com"
            receivers = ['suporte@roandigital.com']
            message = MIMEText(
                mensagem + os.linesep + "Application: %s" % app_name)
            message[
                'Subject'] = "Feedback Semard - %s" % socket.gethostname()
            message['From'] = " %s <%s>" % (nome, email)
            message['To'] = "Suporte <suporte@roandigital.com>"

            conn = smtplib.SMTP("smtp.roandigital.com:587")
            conn.login("suporte@roandigital.com", "erros1234")
            conn.sendmail(sender, receivers, message.as_string())
            conn.quit()
            self.com.mBox.emit(
                'O email foi enviado com sucesso. \n\nObrigado pelo seu feedback!')
        except Exception as e:
            self.com.mBoxEr.emit(
                'O email não foi enviado.\n\nVerifique sua conexão com a internet.')


class AnimeList():
    def __init__(self, url):
        #try:
        page = open_url(url)
        page_string = page.read().decode('utf-8')
        soup = BeautifulSoup(page_string)
        links = soup.find_all(
            "td", {'class': 'views-field views-field-title active'})
        self.animes = {}
        self.number = 0
        for td in links:
            if isinstance(td, bs4.element.Tag):
                for a in td.children:
                    if isinstance(a, bs4.element.Tag):
                        anime_link = 'http://www.anbient.net' + a['href']
                        anime_name = str(a.string)
                        #print(anime_name)
                        self.animes[anime_name] = anime_link
                        self.number += 1
        #print((self.animes))
        #except Exception as er:
        #    print(er.message)

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
        # Thread.__init__(self)
        self.url = url
        self.episodes = {}
        self.sinopse = None
        self.run()
        # self.start()

    def run(self):
        try:
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
                    if episode_name not in list(self.episodes.keys()):
                        episode = Episode(episode_name)
                        self.episodes[episode_name] = episode
                        self.episodes[episode_name].links.append(episode_link)
                    else:
                        self.episodes[episode_name].links.append(episode_link)
        except Exception as er:
            print((er.message))

    def get_episodes(self):
        return self.episodes

    def get_sinopse(self):
        return self.sinopse


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, com, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        showAction = menu.addAction("Mostrar")
        showAction.triggered.connect(self.show_action)
        exitAction = menu.addAction("Fechar")
        exitAction.triggered.connect(self.close_event)
        self.activated.connect(self.tray_activated)
        self.setContextMenu(menu)
        self.com = com
        self.show()

    def show_action(self):
        self.com.op.emit('open')

    def tray_activated(self, reason):
        if reason is QSystemTrayIcon.DoubleClick:
            self.com.op.emit('open')

    def close_event(self):
        os._exit(-1)


class Feedback(QDialog):
    """Send feedback"""

    def __init__(self, com):
        super(Feedback, self).__init__()
        self.ui = Ui_FeedbackDialog()
        self.ui.setupUi(self)
        self.ui.sendButton.clicked.connect(self.send_mail)
        self.com = com
        self.com.mBox.connect(m_box_exec_success)
        self.com.mBoxEr.connect(m_box_exec)
        self.setWindowIcon(QIcon(get_file('animes.png')))

    def send_mail(self):
        """Calls EmailSender to send the feedback"""
        mail = EmailSender(self.ui.nameEdit.text(), 'Semard',
                           self.ui.emailEdit.text(), self.ui.messageEdit.toPlainText(), self.com)
        mail.start()
        mail.join()
        self.close()


    class Player(QMainWindow):
        """A simple Media Player using VLC and Qt """
        def __init__(self, player, master=None):
            QMainWindow.__init__(self, master)
            self.setWindowTitle("Semard: Mini-Player")

            # creating a basic vlc instance
            #self.instance = vlc.Instance()
            # creating an empty vlc media player
            self.mediaplayer = player  # self.instance.media_player_new()
            self.setWindowIcon(QIcon(get_file('animes.png')))

            #self.ui = self.createUI()
            self.isPaused = False

        def toogleFullscreen(self):
            if self.isFullScreen():
                self.playbutton.show()
                self.reloadbutton.show()
                self.positionslider.show()
                self.volumeslider.show()
                self.menubar.show()
                self.vboxlayout.setContentsMargins(0, 0, 0, 0)
                self.showNormal()
            else:
                self.playbutton.hide()
                self.reloadbutton.hide()
                self.positionslider.hide()
                self.volumeslider.hide()
                self.menubar.hide()
                self.vboxlayout.setContentsMargins(0, 0, 0, 0)
                self.showFullScreen()

        def mouseDoubleClickEvent(self, event):
            # self.mediaplayer.toggle_fullscreen()
            self.toogleFullscreen()

        def setMedia(self, media):
            self.media = media

        def setPlayer(self, player):
            self.mediaplayer = player

        def closeEvent(self, event):
            event.ignore()
            self.exit_media()
            self.hide()

        def createUI(self):
            """Set up the user interface, signals & slots
            """
            self.widget = QtGui.QWidget(self)
            self.setCentralWidget(self.widget)

            # In this widget, the video will be drawn
            self.videoframe = QtGui.QFrame()
            self.palette = self.videoframe.palette()
            self.palette.setColor(QtGui.QPalette.Window,
                                  QtGui.QColor(0, 0, 0))
            self.videoframe.setPalette(self.palette)
            self.videoframe.setAutoFillBackground(True)

            self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
            self.positionslider.setToolTip("Position")
            self.positionslider.setMaximum(1000)
            self.connect(self.positionslider,
                         QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

            self.hbuttonbox = QtGui.QHBoxLayout()
            self.playbutton = QtGui.QPushButton("Play")
            self.hbuttonbox.addWidget(self.playbutton)
            self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                         self.PlayPause)

            self.reloadbutton = QtGui.QPushButton("Reload")
            self.hbuttonbox.addWidget(self.reloadbutton)
            self.connect(self.reloadbutton, QtCore.SIGNAL("clicked()"),
                         self.Reload)
            self.reloadbutton.setEnabled(False)
            self.reloadbutton.hide()

            self.hbuttonbox.addStretch(1)
            self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
            self.volumeslider.setMaximum(100)
            self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
            self.volumeslider.setToolTip("Volume")
            self.hbuttonbox.addWidget(self.volumeslider)
            self.connect(self.volumeslider,
                         QtCore.SIGNAL("valueChanged(int)"),
                         self.setVolume)

            self.vboxlayout = QtGui.QVBoxLayout()
            self.vboxlayout.addWidget(self.videoframe)
            self.vboxlayout.addWidget(self.positionslider)
            self.vboxlayout.addLayout(self.hbuttonbox)

            self.widget.setLayout(self.vboxlayout)

            #open = QtGui.QAction("&Open", self)
            #self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
            ext = QtGui.QAction("&Exit", self)
            self.connect(ext, QtCore.SIGNAL("triggered()"), self.exit_media)
            self.menubar = self.menuBar()
            filemenu = self.menubar.addMenu("&File")
            # filemenu.addAction(open)
            filemenu.addSeparator()
            filemenu.addAction(ext)

            self.timer = QtCore.QTimer(self)
            self.timer.setInterval(200)
            self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                         self.updateUI)

        def Reload(self):
            self.mediaplayer.release()
            self.mediaplayer.set_media(self.media)
            self.media.parse()
            self.mediaplayer.play()

        def exit_media(self):
            self.mediaplayer.stop()
            self.close()

        def PlayPause(self):
            """Toggle play/pause status
            """
            if self.mediaplayer.is_playing():
                self.mediaplayer.pause()
                self.playbutton.setText("Play")
                self.isPaused = True
            else:
                if self.mediaplayer.play() == -1:
                    # self.OpenFile()
                    return
                self.mediaplayer.play()
                self.playbutton.setText("Pause")
                self.timer.start()
                self.isPaused = False

        def Stop(self):
            """Stop player
            """
            self.mediaplayer.stop()
            self.playbutton.setText("Play")

        def OpenFile(self, filename=None):
            """Open a media file in a MediaPlayer
            """
            if filename is None:
                filename = QFileDialog.getOpenFileName(
                    self, "Open File", os.path.expanduser("~"))
            if not filename:
                return

            # create the media
            self.mediaplayer = self.instance.media_player_new()
            # put the media in the media player
            self.mediaplayer.set_media(self.media)
            # parse the metadata of the file
            self.media.parse()
            # set the title of the track as window title
            self.setWindowTitle(self.media.get_meta(0))

            # the media player has to be 'connected' to the QFrame
            # (otherwise a video would be displayed in it's own window)
            # this is platform specific!
            # you have to give the id of the QFrame (or similar object) to
            # vlc, different platforms have different functions for this
            if sys.platform == "linux2":  # for Linux using the X Server
                self.mediaplayer.set_xwindow(self.videoframe.winId())
            elif sys.platform == "win32":  # for Windows
                self.mediaplayer.set_hwnd(self.videoframe.winId())
            elif sys.platform == "darwin":  # for MacOS
                self.mediaplayer.set_agl(self.videoframe.windId())
            self.PlayPause()

        def setVolume(self, Volume):
            """Set the volume
            """
            self.mediaplayer.audio_set_volume(Volume)

        def setPosition(self, position):
            """Set the position
            """
            # setting the position to where the slider was dragged
            self.mediaplayer.set_position(position / 1000.0)
            # the vlc MediaPlayer needs a float value between 0 and 1, Qt
            # uses integer variables, so you need a factor; the higher the
            # factor, the more precise are the results
            # (1000 should be enough)

        def updateUI(self):
            """updates the user interface"""
            # setting the slider to the desired position
            self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

            if not self.mediaplayer.is_playing():
                # no need to call this function if nothing is played
                self.timer.stop()
                if not self.isPaused:
                    # after the video finished, the play button stills shows
                    # "Pause", not the desired behavior of a media player
                    # this will fix it
                    self.Stop()


class Browser(QDialog):
    start_download = Signal(str, str)
    open_video = Signal(str, bool)

    def __init__(self):
        super(Browser, self).__init__()
        self.ui = Ui_BrowserWidget()
        self.ui.setupUi(self)
        self.ui.webView.page().setForwardUnsupportedContent(True)
        self.ui.webView.page().unsupportedContent.connect(self.download)
        self.setWindowIcon(QIcon(get_file('animes.png')))
        #self.player_window = player_w

    def showBox(self, text, infoText):
        mbox = QMessageBox()
        mbox.setWindowTitle("Semard")
        mbox.setText(text)
        mbox.setInformativeText(infoText)
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No
                                | QMessageBox.Cancel)
        mbox.setDefaultButton(QMessageBox.Yes)
        return mbox.exec_()


    def download(self, reply):
        filepath = reply.url().toString()
        #dl = self.showBox('Iniciar download de', filepath)
        #if dl == QMessageBox.Yes:
        split = urllib.parse.urlsplit(filepath)
        filename = split.path.split("/")[-1]
        ofd = QFileDialog()
        ofd.setFileMode(QFileDialog.Directory)
        ofd.setOption(QFileDialog.ShowDirsOnly)
        ofd.setWindowTitle(filename)
        if ofd.exec_():
            res = ofd.selectedFiles()[0]
            path = os.path.join(res, filename)
            self.start_download.emit(str(filepath), str(path))
        #elif dl == QMessageBox.No:
        #    pass
        #elif dl == QMessageBox.Cancel:
        #    pass

        rep = self.showBox('Tentar reproduzir o arquivo?', filepath)
        if rep == QMessageBox.Yes:
            self.open_video.emit(filepath, False)
            self.close()
            main.hide()
        elif rep == QMessageBox.No:
            pass
        elif rep == QMessageBox.Cancel:
            pass


class Downloader(QObject):
    progresschanged = Signal(float, QProgressBar)
    started = Signal(str)
    finished = Signal(QProgressBar, str)

    def __init__(self, url, filename, progressbar):
        QObject.__init__(self)
        self.url = url
        self.filename = filename
        self.progressbar = progressbar

    def download(self):
        self.started.emit(self.filename)
        self.curl_download(self.url, self.filename)

    def curl_download(self, url, filename):
        """Rate limit in bytes"""
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        #c.setopt(c.MAX_RECV_SPEED_LARGE, rate_limit)
        if os.path.exists(filename):
            file_id = open(filename, "ab")
            self.current_size = os.path.getsize(filename)
            c.setopt(pycurl.RESUME_FROM, self.current_size)
            self.exists = True
        else:
            file_id = open(filename, "wb")
            self.exists = False
        try:
            c.setopt(pycurl.WRITEDATA, file_id)
            c.setopt(pycurl.NOPROGRESS, 0)
            c.setopt(pycurl.PROGRESSFUNCTION, self.curl_progress)
            c.perform()
            self.finished.emit(self.progressbar, os.path.basename(self.filename))
        except Exception as er:
            print((er.message))

    def curl_progress(self, total, existing, upload_t, upload_d):
        try:
            if self.exists:
                frac = ((float(existing) + float(self.current_size)) / (float(total) + float(self.current_size))) * 100
            else:
                frac = (float(existing) / float(total)) * 100
            self.progresschanged.emit(frac, self.progressbar)
            #if frac == float(100) and total != 0 and existing != 0:
            #    self.finished.emit(self.progressbar, os.path.basename(self.filename))
        except:
            frac = 0
            #print("Downloaded %d/%d (%0.2f%%)" % (existing, total, frac))


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
        #self.load_url_items()
        self.movie = QMovie(get_file('ajax-loader.gif'))
        self.ui.loading_label.setMovie(self.movie)
        self.link = None
        self.main_download_page = None
        self.tray = SystemTrayIcon(
            QIcon(get_file('animes.png')), self.com, self)
        self.com.op.connect(self.show_semard)
        self.ui.action_About_Semard.triggered.connect(self.about_semard)
        self.ui.action_Contato.triggered.connect(self.show_feedback)
        self.setWindowTitle('Semard - Animes')
        self.browser = None
        self.player = None
        #self.player_window = player_w

    @Slot(str, bool)
    def openVideo(self, filepath, duplicate_mode):
        movie = os.path.expanduser(filepath)
        if 'http://' not in filepath:
            if not os.access(movie, os.R_OK):
                print(('Error: %s file is not readable' % movie))
            sys.exit(1)

        split = urllib.parse.urlsplit(filepath)
        #name = QInputDialog.getText(self, 'Escolha nome do arquivo', 'Nome do arquivo:')
        name = split.path.split("/")[-1]
        #pa = os.path.join(res, name)
        if duplicate_mode:
            try:
                #media = instance.media_new(movie, 'sout=#duplicate{dst=file{dst=%s},dst=display}' % pa)
                pass
            except NameError:
                print(('NameError: % (%s vs Libvlc %s)' % (sys.exc_info()[1],
                                                           vlc.__version__, vlc.libvlc_get_version())))
        else:
            try:
                #media = instance.media_new(movie)
                if sys.platform in 'win32':
                    subprocess.Popen([os.path.join('vlc','vlc'), movie])
                else:
                    subprocess.Popen(['vlc', movie])
            except NameError:
                print(('NameError: % (%s vs Libvlc %s)' % (sys.exc_info()[1],
                                                           vlc.__version__, vlc.libvlc_get_version())))
                QMessageBox.critical(self, 'Erro','problema ao iniciar o vlc')
                # "--sout=#duplicate{dst=file{dst=example.mpg},dst=display}"

        #player = instance.media_player_new()
        #pplayer.set_media(media)
        #self.player_window.setMedia(media)
        #self.player_window.createUI()
        #self.player_window = Player()
        #media.parse()
        #self.player_window.setWindowTitle(media.get_meta(0))
        #self.player_window.show()
        #self.player_window.resize(640, 480)
        #if sys.platform == "linux2":  # for Linux using the X Server
        #    pplayer.set_xwindow(self.player_window.videoframe.winId())
        #elif sys.platform == "win32":  # for Windows
        #    pplayer.set_hwnd(self.player_window.videoframe.winId())
        #elif sys.platform == "darwin":  # for MacOS
        #    pplayer.set_agl(self.player_window.videoframe.windId())
        #pplayer.play()
        #self.player_window.updateUI()

    @Slot(str, str)
    def start_download(self, filepath, path):
        #thread = QThread(self)
        pbar = QProgressBar(self.ui.tab_downloads)
        pbar.setMinimum(0)
        pbar.setMaximum(100)
        pbar.setValue(0)
        self.ui.formLayout.addRow(os.path.basename(path), pbar)
        pbar.show()
        dw = Downloader(str(filepath), str(path), pbar)
        dw.finished.connect(self.finished_download)
        dw.progresschanged.connect(self.show_download_progress)
        dw.started.connect(self.started_download)
        Thread(target=dw.download).start()
        #thread.started.connect(dw.download)
        #thread.finished.connect(self.finished_download)
        #dw.moveToThread(thread)
        #thread.start()

    def finished_download(self, pbar, filename):
        self.tray.showMessage(filename, 'Download concluído.')
        pbar.setValue(100)
        pbar.setEnabled(False)

    def started_download(self, filename):
        filename = os.path.basename(filename)
        self.tray.showMessage(filename, 'Download iniciado.')

    @Slot(float, QProgressBar)
    def show_download_progress(self, progress, pbar):
        pbar.setValue(progress)

    def show_feedback(self):
        feed = Feedback(self.com)
        feed.exec_()

    def about_semard(self):
        about = QMessageBox.about(self, "Sobre Semard",
                                  """<b>Semard</b> v%s
        <p><b>Copyright (C) 2013</b> Ronnie Andrew.</p>
        <p>Todos os direitos reservados de acordo com a licença GNU GPL v3 ou posterior.</p>
        <p><b>Website Oficial:</b> <a href='https://github.com/ROAND/Series-Manager'>GitHub</a></p>
        <p><b>Plataforma: </b>%s</p>
          """ % (__version__, platform.system()))

    def show_semard(self, message):
        self.show()

    def closeEvent(self, event):
        self.hide()
        self.tray.showMessage('Semard', 'Semard ainda está em execução.')
        event.ignore()

    @Slot(str)
    def set_image(self, img_str):
        self.ui.image_label.setPixmap(QPixmap(img_str))

    @Slot(str)
    def message(self, message):
        if str(message) in 'ended':
            self.ui.loading_label.hide()
            # self.repaint()
            self.ui.anime_list_widget.setEnabled(True)
            self.ui.show_button.setEnabled(True)
            self.movie.stop()
        if str(message) in 'started':
            self.ui.loading_label.show()
            # self.repaint()
            self.ui.anime_list_widget.setEnabled(False)
            self.ui.show_button.setEnabled(False)
            self.movie.start()

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
        link = self.ui.options_list_widget.currentItem().text()
        self.com.sig.emit('started')
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Informação')
        msgBox.setText('Browser padrão')
        msgBox.setInformativeText(
            'Você deseja abrir este link com o seu browser padrão?')
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.Yes)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            if sys.platform in 'win32':
                webbrowser.open(link)
            else:
                webbrowser.open(link)
        else:
            browser.ui.webView.setUrl(QUrl(link))
            browser.show()
        self.com.sig.emit('ended')

    def keyPressEvent(self, event):
        if isinstance(event, PyQt5.QtGui.QKeyEvent):
            if event.key() == Qt.Key_Down:
                self.ui.anime_list_widget.setCurrentRow(
                    self.ui.anime_list_widget.currentRow() + 1)
            elif event.key() == Qt.Key_Up:
                self.ui.anime_list_widget.setCurrentRow(
                    self.ui.anime_list_widget.currentRow() - 1)

    @staticmethod
    def get_img_link(url):
        page = urllib.request.urlopen(url)
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
        # self.episodes.join()
        self.link = self.get_img_link(link)
        self.episode_list = self.episodes.get_episodes()

        anime_name = self.ui.anime_list_widget.currentItem().text()
        link = self.anime_list[anime_name]
        img_link = self.get_img_link(link)
        file_name = img_link
        if os.path.exists(get_file(file_name)):
            self.com.img.emit(get_file(file_name))
            # self.ui.image_label.setPixmap(QPixmap(get_file(file_name)))
        else:
            if img_link is not None:
                file_name = img_link.replace(
                    'http://www.anbient.net/sites/default/files/imagecache/242x0/imagens/poster/', '')
                urllib.request.urlretrieve(
                    'http://www.anbient.net/sites/default/files/imagecache/242x0/imagens/poster/%s' % file_name,
                    get_file(file_name))
                self.com.img.emit(get_file(file_name))
                # self.ui.image_label.setPixmap(QPixmap(get_file(file_name)))

        self.ui.label_sinopse.setText(self.episodes.get_sinopse().strip())
        try:
            for name in reversed(sorted(list(self.episode_list.keys()), key=int)):
                episode = self.episode_list[name]
                name, links = episode.get_attrs()
                self.ui.res_list_widget.addItem(name)
        except:
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

    def setBrowser(self, browser_param):
        self.browser = browser_param
        self.browser.start_download.connect(self.start_download)
        self.browser.open_video.connect(self.openVideo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #instance = vlc.Instance()
    #pplayer = instance.media_player_new()
    #player_w = Player(pplayer)
    main = MainWindow()
    browser = Browser()
    main.setBrowser(browser)
    main.show()
    sys.exit(app.exec_())

import sys
import urllib.request
import socket
import re
from html.parser import HTMLParser
from views.main_ui_pyside import Ui_MainWindow
import PySide
from PySide.QtGui import QApplication, QWidget, QMainWindow
from PySide.QtCore import Qt

timeout = 10
socket.setdefaulttimeout(timeout)

#f = open('animelist.html','r')
#page_string = f.read()
#print(page_string)

class PageProcessList():
    def __init__(self):
        self.page = urllib.request.urlopen("http://www.animetake.com/anime-downloads/")
        self.page_string = self.page.read().decode('utf-8')
        
    def load_items(self):
        anime_links_names = re.findall(r'<li\b[^>]*>(.*?)</li>', self.page_string)
        anime_names = []
        anime_database = {}
        for string in anime_links_names:
            link = None
            name = None
            link = re.findall(r'href="(.*?)"', string)
            name = re.findall(r'<a\b[^>]*>(.*?)</a>', string)[0] #findall returns a list
            anime_names.append(name)
            if link != [] and link is not None:
                anime_database[name] = link[0]
        return anime_database, anime_names

        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.process = PageProcessList()
        self.ui.searchEdit.textChanged.connect(self.search_text_changed)
        self.add_full_items_animelist()

    def add_full_items_animelist(self):
        anime_database, anime_names = self.process.load_items()
        self.ui.anime_list_widget.clear()
        for name, link in sorted(anime_database.items()):
            self.ui.anime_list_widget.addItem(name)

    def search_text_changed(self, newText):
        items = self.ui.anime_list_widget.findItems(newText, Qt.MatchContains)
        if items != []:
            self.ui.anime_list_widget.setCurrentItem(items[0])
            self.ui.labelSearch.setText('')
        else:
            self.ui.labelSearch.setText('Not Found!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

# create a subclass and override the handler methods
#class Parser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#         pass
#
#    def handle_endtag(self, tag):
#         pass
#
#    def handle_data(self, data):
#        pass
#
#parser = Parser()
#parser.feed(page_string)

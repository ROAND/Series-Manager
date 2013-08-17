'''
Created on Jul 13, 2013

@author: Roan Digital
'''
#-*- coding: utf-8 -*-
import sys
from PySide import QtGui
from views.seriesmanagerUI import Ui_MainWindow

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None): #Construtor da classe MainWindow que chama a classe Ui_MainWindow gerada pelo pyside-uic
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow() #Equivalente a: Ui_MainWindow ui = new Ui_MainWindow(); no java ou C# ou C++
        self.ui.setupUi(self) #Da as caracteristicas do Ui_MainWindow a classe MainWindow
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) #Declara um aplicativo Qt
    main = MainWindow()
    main.setWindowTitle("Series Manager")
    main.show()
    sys.exit(app.exec_())
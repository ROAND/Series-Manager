# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browser.ui'
#
# Created: Thu Dec  5 06:51:27 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_BrowserWidget(object):
    def setupUi(self, BrowserWidget):
        BrowserWidget.setObjectName("BrowserWidget")
        BrowserWidget.resize(717, 444)
        self.gridLayout = QtGui.QGridLayout(BrowserWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QtWebKit.QWebView(BrowserWidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.retranslateUi(BrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(BrowserWidget)

    def retranslateUi(self, BrowserWidget):
        BrowserWidget.setWindowTitle(QtGui.QApplication.translate("BrowserWidget", "Semard: Mini-Browser", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit

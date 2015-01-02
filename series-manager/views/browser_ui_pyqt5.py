# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browser.ui'
#
# Created: Fri Jan  2 01:55:04 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BrowserWidget(object):
    def setupUi(self, BrowserWidget):
        BrowserWidget.setObjectName("BrowserWidget")
        BrowserWidget.resize(717, 444)
        self.gridLayout = QtWidgets.QGridLayout(BrowserWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QtWebKitWidgets.QWebView(BrowserWidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.retranslateUi(BrowserWidget)
        QtCore.QMetaObject.connectSlotsByName(BrowserWidget)

    def retranslateUi(self, BrowserWidget):
        _translate = QtCore.QCoreApplication.translate
        BrowserWidget.setWindowTitle(_translate("BrowserWidget", "Semard: Mini-Browser"))

from PyQt5 import QtWebKitWidgets

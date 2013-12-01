# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'feedback.ui'
#
# Created: Sun Dec  1 07:29:26 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FeedbackDialog(object):
    def setupUi(self, FeedbackDialog):
        FeedbackDialog.setObjectName("FeedbackDialog")
        FeedbackDialog.resize(306, 267)
        self.gridLayout = QtGui.QGridLayout(FeedbackDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(FeedbackDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(FeedbackDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(FeedbackDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.nameEdit = QtGui.QLineEdit(FeedbackDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameEdit)
        self.emailEdit = QtGui.QLineEdit(FeedbackDialog)
        self.emailEdit.setObjectName("emailEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.emailEdit)
        self.messageEdit = QtGui.QTextEdit(FeedbackDialog)
        self.messageEdit.setObjectName("messageEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.messageEdit)
        self.sendButton = QtGui.QPushButton(FeedbackDialog)
        self.sendButton.setObjectName("sendButton")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.sendButton)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtGui.QLabel(FeedbackDialog)
        self.label_4.setLineWidth(1)
        self.label_4.setMidLineWidth(0)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(FeedbackDialog)
        self.label_5.setText("")
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.retranslateUi(FeedbackDialog)
        QtCore.QMetaObject.connectSlotsByName(FeedbackDialog)

    def retranslateUi(self, FeedbackDialog):
        FeedbackDialog.setWindowTitle(QtGui.QApplication.translate("FeedbackDialog", "Feedback", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FeedbackDialog", "Nome:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FeedbackDialog", "E-mail", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FeedbackDialog", "Mensagem:", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("FeedbackDialog", "Enviar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FeedbackDialog", "Diga-me o que achou do Semard, e ou como posso melhora-lo.", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'feedback.ui'
#
# Created: Fri Jan  2 01:55:04 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FeedbackDialog(object):
    def setupUi(self, FeedbackDialog):
        FeedbackDialog.setObjectName("FeedbackDialog")
        FeedbackDialog.resize(306, 267)
        self.gridLayout = QtWidgets.QGridLayout(FeedbackDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(FeedbackDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(FeedbackDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(FeedbackDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.nameEdit = QtWidgets.QLineEdit(FeedbackDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameEdit)
        self.emailEdit = QtWidgets.QLineEdit(FeedbackDialog)
        self.emailEdit.setObjectName("emailEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.emailEdit)
        self.messageEdit = QtWidgets.QTextEdit(FeedbackDialog)
        self.messageEdit.setObjectName("messageEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.messageEdit)
        self.sendButton = QtWidgets.QPushButton(FeedbackDialog)
        self.sendButton.setObjectName("sendButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.sendButton)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(FeedbackDialog)
        self.label_4.setLineWidth(1)
        self.label_4.setMidLineWidth(0)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(FeedbackDialog)
        self.label_5.setText("")
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.retranslateUi(FeedbackDialog)
        QtCore.QMetaObject.connectSlotsByName(FeedbackDialog)

    def retranslateUi(self, FeedbackDialog):
        _translate = QtCore.QCoreApplication.translate
        FeedbackDialog.setWindowTitle(_translate("FeedbackDialog", "Feedback"))
        self.label.setText(_translate("FeedbackDialog", "Nome:"))
        self.label_2.setText(_translate("FeedbackDialog", "E-mail"))
        self.label_3.setText(_translate("FeedbackDialog", "Mensagem:"))
        self.sendButton.setText(_translate("FeedbackDialog", "Enviar"))
        self.label_4.setText(_translate("FeedbackDialog", "Diga-me o que achou do Semard, e ou como posso melhora-lo."))


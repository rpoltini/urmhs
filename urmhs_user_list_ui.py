# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_user_list.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_user_list_dialog(object):
    def setupUi(self, user_list_dialog):
        user_list_dialog.setObjectName("user_list_dialog")
        user_list_dialog.resize(639, 299)
        self.label = QtWidgets.QLabel(user_list_dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 361, 16))
        self.label.setObjectName("label")
        self.user_list = QtWidgets.QTableWidget(user_list_dialog)
        self.user_list.setGeometry(QtCore.QRect(10, 30, 541, 231))
        self.user_list.setObjectName("user_list")
        self.user_list.setColumnCount(0)
        self.user_list.setRowCount(0)
        self.buttonBox = QtWidgets.QDialogButtonBox(user_list_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(370, 270, 261, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Help)
        self.buttonBox.setObjectName("buttonBox")
        self.addButton = QtWidgets.QPushButton(user_list_dialog)
        self.addButton.setGeometry(QtCore.QRect(560, 30, 71, 23))
        self.addButton.setObjectName("addButton")
        self.updButton = QtWidgets.QPushButton(user_list_dialog)
        self.updButton.setGeometry(QtCore.QRect(560, 60, 71, 23))
        self.updButton.setObjectName("updButton")
        self.delButton = QtWidgets.QPushButton(user_list_dialog)
        self.delButton.setGeometry(QtCore.QRect(560, 90, 71, 23))
        self.delButton.setObjectName("delButton")

        self.retranslateUi(user_list_dialog)
        self.addButton.clicked.connect(user_list_dialog.onAdd)
        self.updButton.clicked.connect(user_list_dialog.onUpd)
        self.delButton.clicked.connect(user_list_dialog.onDel)
        self.buttonBox.clicked['QAbstractButton*'].connect(user_list_dialog.onButtonBox)
        QtCore.QMetaObject.connectSlotsByName(user_list_dialog)

    def retranslateUi(self, user_list_dialog):
        _translate = QtCore.QCoreApplication.translate
        user_list_dialog.setWindowTitle(_translate("user_list_dialog", "URMHS - User list"))
        self.label.setText(_translate("user_list_dialog", "User list (the yellow row refers to the current user):"))
        self.addButton.setText(_translate("user_list_dialog", "Add..."))
        self.updButton.setText(_translate("user_list_dialog", "Update..."))
        self.delButton.setText(_translate("user_list_dialog", "Delete"))


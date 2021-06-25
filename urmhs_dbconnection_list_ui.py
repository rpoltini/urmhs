# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_dbconnection_list.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dbconnection_list_dialog(object):
    def setupUi(self, dbconnection_list_dialog):
        dbconnection_list_dialog.setObjectName("dbconnection_list_dialog")
        dbconnection_list_dialog.resize(560, 177)
        self.buttonBox = QtWidgets.QDialogButtonBox(dbconnection_list_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 140, 541, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(dbconnection_list_dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 361, 16))
        self.label.setObjectName("label")
        self.dbconnection_list = QtWidgets.QTableWidget(dbconnection_list_dialog)
        self.dbconnection_list.setGeometry(QtCore.QRect(10, 20, 541, 111))
        self.dbconnection_list.setObjectName("dbconnection_list")
        self.dbconnection_list.setColumnCount(0)
        self.dbconnection_list.setRowCount(0)

        self.retranslateUi(dbconnection_list_dialog)
        self.buttonBox.accepted.connect(dbconnection_list_dialog.accept)
        self.buttonBox.rejected.connect(dbconnection_list_dialog.reject)
        self.buttonBox.helpRequested.connect(dbconnection_list_dialog.onHelpButton)
        QtCore.QMetaObject.connectSlotsByName(dbconnection_list_dialog)

    def retranslateUi(self, dbconnection_list_dialog):
        _translate = QtCore.QCoreApplication.translate
        dbconnection_list_dialog.setWindowTitle(_translate("dbconnection_list_dialog", "URMHS - Select a DB connection"))
        self.label.setText(_translate("dbconnection_list_dialog", "DB connection list (the yellow row refers to the current connection):"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_wrk_session_list.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wrk_session_list_dialog(object):
    def setupUi(self, wrk_session_list_dialog):
        wrk_session_list_dialog.setObjectName("wrk_session_list_dialog")
        wrk_session_list_dialog.resize(645, 302)
        self.buttonBox = QtWidgets.QDialogButtonBox(wrk_session_list_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(370, 270, 261, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(wrk_session_list_dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 361, 16))
        self.label_2.setObjectName("label_2")
        self.wrk_session_list = QtWidgets.QTableWidget(wrk_session_list_dialog)
        self.wrk_session_list.setGeometry(QtCore.QRect(10, 30, 621, 231))
        self.wrk_session_list.setObjectName("wrk_session_list")
        self.wrk_session_list.setColumnCount(0)
        self.wrk_session_list.setRowCount(0)
        self.label = QtWidgets.QLabel(wrk_session_list_dialog)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(20, 270, 61, 16))
        self.label.setObjectName("label")
        self.FilterBy = QtWidgets.QComboBox(wrk_session_list_dialog)
        self.FilterBy.setGeometry(QtCore.QRect(78, 270, 141, 21))
        self.FilterBy.setObjectName("FilterBy")
        self.Details = QtWidgets.QPushButton(wrk_session_list_dialog)
        self.Details.setGeometry(QtCore.QRect(230, 270, 75, 23))
        self.Details.setObjectName("Details")

        self.retranslateUi(wrk_session_list_dialog)
        self.buttonBox.accepted.connect(wrk_session_list_dialog.accept)
        self.buttonBox.rejected.connect(wrk_session_list_dialog.reject)
        self.buttonBox.helpRequested.connect(wrk_session_list_dialog.onHelpButton)
        self.FilterBy.currentIndexChanged['int'].connect(wrk_session_list_dialog.onFilterChanged)
        self.Details.clicked.connect(wrk_session_list_dialog.onDetailsButton)
        QtCore.QMetaObject.connectSlotsByName(wrk_session_list_dialog)

    def retranslateUi(self, wrk_session_list_dialog):
        _translate = QtCore.QCoreApplication.translate
        wrk_session_list_dialog.setWindowTitle(_translate("wrk_session_list_dialog", "URMHS - Work session list"))
        self.label_2.setText(_translate("wrk_session_list_dialog", "Work session list (the yellow row refers to the current work session):"))
        self.label.setText(_translate("wrk_session_list_dialog", "Filter by:"))
        self.Details.setText(_translate("wrk_session_list_dialog", "Details..."))


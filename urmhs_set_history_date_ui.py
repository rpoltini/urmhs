# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_set_history_date.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_set_history_date_dialog(object):
    def setupUi(self, set_history_date_dialog):
        set_history_date_dialog.setObjectName("set_history_date_dialog")
        set_history_date_dialog.resize(214, 50)
        set_history_date_dialog.setMinimumSize(QtCore.QSize(214, 50))
        self.dateTime = QtWidgets.QDateTimeEdit(set_history_date_dialog)
        self.dateTime.setGeometry(QtCore.QRect(10, 20, 131, 22))
        self.dateTime.setCalendarPopup(True)
        self.dateTime.setObjectName("dateTime")
        self.set = QtWidgets.QPushButton(set_history_date_dialog)
        self.set.setGeometry(QtCore.QRect(150, 20, 51, 23))
        self.set.setObjectName("set")

        self.retranslateUi(set_history_date_dialog)
        self.set.clicked.connect(set_history_date_dialog.onSetHistoryDate)
        QtCore.QMetaObject.connectSlotsByName(set_history_date_dialog)

    def retranslateUi(self, set_history_date_dialog):
        _translate = QtCore.QCoreApplication.translate
        set_history_date_dialog.setWindowTitle(_translate("set_history_date_dialog", "URMHS - Set history date"))
        self.set.setText(_translate("set_history_date_dialog", "Set"))


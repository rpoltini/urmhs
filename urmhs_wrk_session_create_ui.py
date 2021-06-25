# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_wrk_session_create.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wrk_session_create_dialog(object):
    def setupUi(self, wrk_session_create_dialog):
        wrk_session_create_dialog.setObjectName("wrk_session_create_dialog")
        wrk_session_create_dialog.setWindowModality(QtCore.Qt.WindowModal)
        wrk_session_create_dialog.resize(290, 268)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wrk_session_create_dialog.sizePolicy().hasHeightForWidth())
        wrk_session_create_dialog.setSizePolicy(sizePolicy)
        wrk_session_create_dialog.setMinimumSize(QtCore.QSize(290, 268))
        wrk_session_create_dialog.setMaximumSize(QtCore.QSize(290, 268))
        wrk_session_create_dialog.setWhatsThis("")
        wrk_session_create_dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(wrk_session_create_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 230, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.wrk_session_name = QtWidgets.QLineEdit(wrk_session_create_dialog)
        self.wrk_session_name.setGeometry(QtCore.QRect(70, 20, 211, 20))
        self.wrk_session_name.setObjectName("wrk_session_name")
        self.label = QtWidgets.QLabel(wrk_session_create_dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(wrk_session_create_dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 61, 21))
        self.label_2.setObjectName("label_2")
        self.wrk_session_descr = QtWidgets.QTextEdit(wrk_session_create_dialog)
        self.wrk_session_descr.setGeometry(QtCore.QRect(10, 70, 271, 41))
        self.wrk_session_descr.setObjectName("wrk_session_descr")
        self.label_3 = QtWidgets.QLabel(wrk_session_create_dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 47, 21))
        self.label_3.setObjectName("label_3")
        self.wrk_session_executor = QtWidgets.QComboBox(wrk_session_create_dialog)
        self.wrk_session_executor.setGeometry(QtCore.QRect(70, 130, 211, 22))
        self.wrk_session_executor.setObjectName("wrk_session_executor")
        self.label_4 = QtWidgets.QLabel(wrk_session_create_dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 101, 21))
        self.label_4.setObjectName("label_4")
        self.wrk_session_note = QtWidgets.QTextEdit(wrk_session_create_dialog)
        self.wrk_session_note.setGeometry(QtCore.QRect(10, 180, 271, 41))
        self.wrk_session_note.setObjectName("wrk_session_note")

        self.retranslateUi(wrk_session_create_dialog)
        self.buttonBox.accepted.connect(wrk_session_create_dialog.accept)
        self.buttonBox.rejected.connect(wrk_session_create_dialog.reject)
        self.buttonBox.helpRequested.connect(wrk_session_create_dialog.onHelpButton)
        QtCore.QMetaObject.connectSlotsByName(wrk_session_create_dialog)

    def retranslateUi(self, wrk_session_create_dialog):
        _translate = QtCore.QCoreApplication.translate
        wrk_session_create_dialog.setWindowTitle(_translate("wrk_session_create_dialog", "URMHS - Work session creation"))
        self.label.setText(_translate("wrk_session_create_dialog", "Name:"))
        self.label_2.setText(_translate("wrk_session_create_dialog", "Description:"))
        self.label_3.setText(_translate("wrk_session_create_dialog", "Executer:"))
        self.label_4.setText(_translate("wrk_session_create_dialog", "Note for executer:"))


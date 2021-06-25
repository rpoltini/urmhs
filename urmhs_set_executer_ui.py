# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_set_executer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SetExecuterDialog(object):
    def setupUi(self, SetExecuterDialog):
        SetExecuterDialog.setObjectName("SetExecuterDialog")
        SetExecuterDialog.resize(375, 139)
        self.buttonBox = QtWidgets.QDialogButtonBox(SetExecuterDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.user_comboBox = QtWidgets.QComboBox(SetExecuterDialog)
        self.user_comboBox.setGeometry(QtCore.QRect(120, 10, 241, 22))
        self.user_comboBox.setObjectName("user_comboBox")
        self.note_plainTextEdit = QtWidgets.QPlainTextEdit(SetExecuterDialog)
        self.note_plainTextEdit.setGeometry(QtCore.QRect(120, 40, 241, 41))
        self.note_plainTextEdit.setObjectName("note_plainTextEdit")
        self.label = QtWidgets.QLabel(SetExecuterDialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(SetExecuterDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(SetExecuterDialog)
        self.buttonBox.accepted.connect(SetExecuterDialog.accept)
        self.buttonBox.rejected.connect(SetExecuterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SetExecuterDialog)

    def retranslateUi(self, SetExecuterDialog):
        _translate = QtCore.QCoreApplication.translate
        SetExecuterDialog.setWindowTitle(_translate("SetExecuterDialog", "URMHS - Set executer"))
        self.label.setText(_translate("SetExecuterDialog", "Note:"))
        self.label_2.setText(_translate("SetExecuterDialog", "New executer:"))


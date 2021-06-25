# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_user.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_user_dialog(object):
    def setupUi(self, user_dialog):
        user_dialog.setObjectName("user_dialog")
        user_dialog.resize(400, 217)
        self.buttonBox = QtWidgets.QDialogButtonBox(user_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 180, 361, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.login = QtWidgets.QLineEdit(user_dialog)
        self.login.setGeometry(QtCore.QRect(80, 20, 311, 20))
        self.login.setObjectName("login")
        self.label = QtWidgets.QLabel(user_dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(user_dialog)
        self.groupBox.setGeometry(QtCore.QRect(9, 100, 381, 71))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.label_3.setObjectName("label_3")
        self.security_question = QtWidgets.QLineEdit(self.groupBox)
        self.security_question.setGeometry(QtCore.QRect(120, 10, 251, 20))
        self.security_question.setObjectName("security_question")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.label_2.setObjectName("label_2")
        self.security_answer = QtWidgets.QLineEdit(self.groupBox)
        self.security_answer.setGeometry(QtCore.QRect(120, 40, 251, 20))
        self.security_answer.setObjectName("security_answer")
        self.superuser = QtWidgets.QCheckBox(user_dialog)
        self.superuser.setGeometry(QtCore.QRect(80, 50, 21, 21))
        self.superuser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.superuser.setAutoFillBackground(False)
        self.superuser.setText("")
        self.superuser.setObjectName("superuser")
        self.label_4 = QtWidgets.QLabel(user_dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_4.setObjectName("label_4")
        self.save = QtWidgets.QCheckBox(user_dialog)
        self.save.setGeometry(QtCore.QRect(80, 70, 21, 21))
        self.save.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.save.setAutoFillBackground(False)
        self.save.setText("")
        self.save.setObjectName("save")
        self.label_5 = QtWidgets.QLabel(user_dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(user_dialog)
        self.buttonBox.accepted.connect(user_dialog.accept)
        self.buttonBox.rejected.connect(user_dialog.reject)
        self.buttonBox.helpRequested.connect(user_dialog.onHelpButton)
        self.superuser.clicked.connect(user_dialog.onSuperUser)
        QtCore.QMetaObject.connectSlotsByName(user_dialog)

    def retranslateUi(self, user_dialog):
        _translate = QtCore.QCoreApplication.translate
        user_dialog.setWindowTitle(_translate("user_dialog", "URMHS - User details"))
        self.label.setText(_translate("user_dialog", "Login:"))
        self.label_3.setText(_translate("user_dialog", "Security answer:"))
        self.label_2.setText(_translate("user_dialog", "Security question:"))
        self.label_4.setText(_translate("user_dialog", "Super user:"))
        self.label_5.setText(_translate("user_dialog", "Save:"))


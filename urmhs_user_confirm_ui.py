# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_user_confirm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_user_confirm_dialog(object):
    def setupUi(self, user_confirm_dialog):
        user_confirm_dialog.setObjectName("user_confirm_dialog")
        user_confirm_dialog.resize(361, 216)
        self.buttonBox = QtWidgets.QDialogButtonBox(user_confirm_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 180, 321, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(user_confirm_dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 70, 341, 101))
        self.groupBox.setObjectName("groupBox")
        self.current_login = QtWidgets.QLabel(user_confirm_dialog)
        self.current_login.setGeometry(QtCore.QRect(110, 50, 181, 21))
        self.current_login.setObjectName("current_login")
        self.label_2 = QtWidgets.QLabel(user_confirm_dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.label_2.setObjectName("label_2")
        self.security_answer = QtWidgets.QLineEdit(user_confirm_dialog)
        self.security_answer.setGeometry(QtCore.QRect(120, 140, 221, 21))
        self.security_answer.setObjectName("security_answer")
        self.label_4 = QtWidgets.QLabel(user_confirm_dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 90, 91, 21))
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.security_question = QtWidgets.QLabel(user_confirm_dialog)
        self.security_question.setGeometry(QtCore.QRect(120, 90, 221, 41))
        self.security_question.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.security_question.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.security_question.setWordWrap(True)
        self.security_question.setObjectName("security_question")
        self.label_6 = QtWidgets.QLabel(user_confirm_dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 140, 91, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(user_confirm_dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 341, 41))
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(user_confirm_dialog)
        self.buttonBox.accepted.connect(user_confirm_dialog.accept)
        self.buttonBox.rejected.connect(user_confirm_dialog.reject)
        self.buttonBox.helpRequested.connect(user_confirm_dialog.onHelpButton)
        QtCore.QMetaObject.connectSlotsByName(user_confirm_dialog)

    def retranslateUi(self, user_confirm_dialog):
        _translate = QtCore.QCoreApplication.translate
        user_confirm_dialog.setWindowTitle(_translate("user_confirm_dialog", "URMHS - Identity confirmation"))
        self.groupBox.setTitle(_translate("user_confirm_dialog", "Security settings"))
        self.current_login.setText(_translate("user_confirm_dialog", "TextLabel"))
        self.label_2.setText(_translate("user_confirm_dialog", "Current login:"))
        self.label_4.setText(_translate("user_confirm_dialog", "Security question:"))
        self.security_question.setText(_translate("user_confirm_dialog", "TextLabel"))
        self.label_6.setText(_translate("user_confirm_dialog", "Security answer:"))
        self.label_7.setText(_translate("user_confirm_dialog", "If you suspect that another user with the same login is working on the same DB, confirm your identity to URHMS."))


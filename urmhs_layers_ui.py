# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_layers.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(475, 382)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 350, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layer_list = QtWidgets.QListView(Dialog)
        self.layer_list.setGeometry(QtCore.QRect(10, 30, 451, 301))
        self.layer_list.setObjectName("layer_list")
        self.add_new_layer = QtWidgets.QCheckBox(Dialog)
        self.add_new_layer.setGeometry(QtCore.QRect(10, 340, 181, 17))
        self.add_new_layer.setObjectName("add_new_layer")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.update_map_2 = QtWidgets.QCheckBox(Dialog)
        self.update_map_2.setGeometry(QtCore.QRect(10, 360, 181, 17))
        self.update_map_2.setObjectName("update_map_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_new_layer.setText(_translate("Dialog", "Add new urmhs layers to map"))
        self.label.setText(_translate("Dialog", "Layer list"))
        self.update_map_2.setText(_translate("Dialog", "Remove original layers to map"))


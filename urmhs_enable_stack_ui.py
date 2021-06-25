# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'urmhs_enable_stack.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_enable_stack(object):
    def setupUi(self, enable_stack):
        enable_stack.setObjectName("enable_stack")
        enable_stack.resize(451, 474)
        enable_stack.setMinimumSize(QtCore.QSize(451, 474))
        enable_stack.setMaximumSize(QtCore.QSize(451, 474))
        self.buttonBox = QtWidgets.QDialogButtonBox(enable_stack)
        self.buttonBox.setGeometry(QtCore.QRect(190, 440, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.addToMap = QtWidgets.QCheckBox(enable_stack)
        self.addToMap.setGeometry(QtCore.QRect(10, 400, 301, 17))
        self.addToMap.setChecked(True)
        self.addToMap.setObjectName("addToMap")
        self.label = QtWidgets.QLabel(enable_stack)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 16))
        self.label.setObjectName("label")
        self.layerTree = QtWidgets.QTreeWidget(enable_stack)
        self.layerTree.setGeometry(QtCore.QRect(10, 30, 431, 361))
        self.layerTree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.layerTree.setObjectName("layerTree")
        self.layerTree.headerItem().setText(0, "1")
        self.layerTree.header().setVisible(False)
        self.removeFromMap = QtWidgets.QCheckBox(enable_stack)
        self.removeFromMap.setGeometry(QtCore.QRect(10, 420, 301, 17))
        self.removeFromMap.setChecked(True)
        self.removeFromMap.setObjectName("removeFromMap")

        self.retranslateUi(enable_stack)
        self.buttonBox.accepted.connect(enable_stack.accept)
        self.buttonBox.rejected.connect(enable_stack.reject)
        self.layerTree.itemChanged['QTreeWidgetItem*','int'].connect(enable_stack.onItemChanged)
        QtCore.QMetaObject.connectSlotsByName(enable_stack)

    def retranslateUi(self, enable_stack):
        _translate = QtCore.QCoreApplication.translate
        enable_stack.setWindowTitle(_translate("enable_stack", "Dialog"))
        self.addToMap.setText(_translate("enable_stack", "Add to map new stack enabled layers"))
        self.label.setText(_translate("enable_stack", "Layers that can be stack enabled:"))
        self.removeFromMap.setText(_translate("enable_stack", "Remove from map original layers"))


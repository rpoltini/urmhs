# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 user list

                              -------------------
        begin                : 2019-12-12
        email                : roberto.poltini@gmail.com
        developers           : roberto poltini
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QApplication, QDialog, QMessageBox, QAbstractItemView, QTableWidgetItem, QHeaderView, QDialogButtonBox
from qgis.core import *
from qgis.gui import *

from .urmhs_user_dlg import urmhsUser_Dialog, urmhsUserDlgModeEnum
from . import urmhs_user_list_ui
from . import urmhs_users
from .urmhs_help import showHelp


#######################################################################################
# Classe che gestisce l'interfaccia grafica per la lista degli utenti
class urmhsUserList_Dialog(QDialog, QObject, urmhs_user_list_ui.Ui_user_list_dialog):
   def __init__(self, parent, conn):
      QDialog.__init__(self, parent)
      self.conn = conn
      self.count = 0
      self.setupUi()
      self.load_from_db()
      self.OrderedCol = 0
      self.colOrderType = Qt.AscendingOrder


   def setupUi(self):
      urmhs_user_list_ui.Ui_user_list_dialog.setupUi(self, self)
      
      self.user_list.setAlternatingRowColors(True)
      self.user_list.setStyleSheet("alternate-background-color: lightGray")
      self.user_list.setColumnCount(5)
      headerLabels = []
      headerLabels.append(QApplication.translate("urmhs", "Login"))
      headerLabels.append(QApplication.translate("urmhs", "Super user"))
      headerLabels.append(QApplication.translate("urmhs", "Grant for save"))
      headerLabels.append(QApplication.translate("urmhs", "Security question"))
      headerLabels.append(QApplication.translate("urmhs", "Security answer"))

      self.user_list.setSelectionBehavior(QAbstractItemView.SelectRows)
      self.user_list.setSelectionMode(QAbstractItemView.SingleSelection)

      self.user_list.setHorizontalHeaderLabels(headerLabels)
      self.user_list.horizontalHeader().show()
      self.user_list.verticalHeader().hide()

      hHeader = self.user_list.horizontalHeader()
      hHeader.sectionClicked[int].connect(self.on_sectionClicked)


   def load_from_db(self):
      # ricavo l'utente corrente
      uri = QgsDataSourceUri(self.conn.dsn)
      currentUser = uri.username()
            
      if self.user_list.model() is not None:
         # Pulisce la tabella
         self.user_list.clearContents()
         self.user_list.setRowCount(0)

      self.count = 0
      obj = urmhs_users.urmhsUserListClass(self.conn)

      obj.load_from_db()
      for user in obj.userList:
         self.insertRow(user)

      self.OrderedCol = 0
      self.colOrderType = Qt.AscendingOrder
      self.user_list.sortItems(0, Qt.AscendingOrder)

      hHeader = self.user_list.horizontalHeader()
      hHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
      hHeader.setStretchLastSection(True)
      
      if currentUser is not None:
         for row in range(0, self.user_list.rowCount()):
            item = self.user_list.item(row, 0)
            if currentUser == item.data(Qt.DisplayRole):
               self.user_list.setCurrentCell(row, 0, QItemSelectionModel.SelectCurrent)
               for col in range(0, self.user_list.columnCount()):
                  self.user_list.item(row, col).setBackground(Qt.yellow)
               self.user_list.setFocus(Qt.OtherFocusReason)         
      

   def insertRow(self, user):
      self.user_list.insertRow(self.count)
      
      item = QTableWidgetItem()
      item.setData(Qt.DisplayRole, user.login)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.user_list.setItem(self.count, 0, item)

      item = QTableWidgetItem()
      item.data(Qt.CheckStateRole);
      if user.isSuperUser:
         item.setCheckState(Qt.Checked)
         item.setText(QApplication.translate("urmhs", "super user"))
      else:
         item.setCheckState(Qt.Unchecked)
         item.setText(QApplication.translate("urmhs", "user"))
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.user_list.setItem(self.count, 1, item)
      
      item = QTableWidgetItem()
      item.data(Qt.CheckStateRole);
      if user.canSave:
         item.setCheckState(Qt.Checked)
         item.setText(QApplication.translate("urmhs", "can save"))
      else:
         item.setCheckState(Qt.Unchecked)
         item.setText(QApplication.translate("urmhs", "can ask for approval"))
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.user_list.setItem(self.count, 2, item)

      item = QTableWidgetItem(user.security_question)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.user_list.setItem(self.count, 3, item)
      
      item = QTableWidgetItem("********")
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.user_list.setItem(self.count, 4, item)
      
      self.count += 1


   def on_sectionClicked(self, i):
      if i != self.OrderedCol:
         self.OrderedCol = i
         self.colOrderType = Qt.AscendingOrder
      else:
         self.colOrderType = Qt.AscendingOrder if self.colOrderType == Qt.DescendingOrder else Qt.DescendingOrder
         
      self.user_list.sortItems(self.OrderedCol, self.colOrderType)
         

   def getSelectUserLogin(self):
      sm = self.user_list.selectionModel()
      if sm.hasSelection() == False:
         return None
      selectedRow = sm.selection().indexes()[0].row()
      item = self.user_list.item(selectedRow, 0)
      return item.data(Qt.DisplayRole)


   def onButtonBox(self, button):
      if button == self.buttonBox.button(QDialogButtonBox.Close):
         QDialog.close(self)
      elif button == self.buttonBox.button(QDialogButtonBox.Help):
         showHelp(QApplication.translate("Help", "User management"))
      

   def onUpd(self):
      user_login = self.getSelectUserLogin()
      if user_login is None:
         return

      obj = urmhs_users.urmhsUserListClass(self.conn)
      obj.load_from_db("login='" + user_login + "'")
      if len(obj.userList) == 1:
         dlg = urmhsUser_Dialog(None, self.conn, obj.userList[0], urmhsUserDlgModeEnum.UPD)
         if dlg.exec_() == QDialog.Accepted:
            self.load_from_db()


   def onAdd(self):
      dlg = urmhsUser_Dialog(None, self.conn, None, urmhsUserDlgModeEnum.ADD)
      if dlg.exec_() == QDialog.Accepted:
         self.load_from_db()


   def onDel(self):
      user_login = self.getSelectUserLogin()
      if user_login is None:
         return

      msg = QApplication.translate("urmhs", "Are you sure you want to delete the {0} user ?").format(user_login)
      reply = QMessageBox.question(None, "URMHS", msg, QMessageBox.Yes | QMessageBox.No)
      if reply == QMessageBox.Yes:
         obj = urmhs_users.urmhsUserListClass(self.conn)
         if obj.del_user_to_db(user_login) == True:
            self.load_from_db()

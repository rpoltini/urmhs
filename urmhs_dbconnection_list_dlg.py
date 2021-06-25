# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 work session list

                              -------------------
        begin                : 2019-12-11
        email                : 
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
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import QApplication, QDialog, QMessageBox, QAbstractItemView, QHeaderView, QTableWidgetItem

from . import urmhs_dbconnection_list_ui
from .urmhs_help import showHelp


#######################################################################################
# Classe che gestisce l'interfaccia grafica per la lista delle connessioni a DB
class urmhsDBConnectionList_Dialog(QDialog, QObject, urmhs_dbconnection_list_ui.Ui_dbconnection_list_dialog):
   def __init__(self, parent, urmhsLayerGroupList):
      QDialog.__init__(self, parent)
      self.urmhsLayerGroupList = urmhsLayerGroupList
      self.count = 0
      self.setupUi()
      self.OrderedCol = 0
      self.colOrderType = Qt.AscendingOrder
      self.load_dbconnection_list()


   def setupUi(self):
      urmhs_dbconnection_list_ui.Ui_dbconnection_list_dialog.setupUi(self, self)
      
      self.dbconnection_list.setAlternatingRowColors(True)
      self.dbconnection_list.setStyleSheet("alternate-background-color: lightGray")
      self.dbconnection_list.setColumnCount(4)
      headerLabels = []
      headerLabels.append(QApplication.translate("urmhs", "Host"))
      headerLabels.append(QApplication.translate("urmhs", "Port"))
      headerLabels.append(QApplication.translate("urmhs", "Database"))
      headerLabels.append(QApplication.translate("urmhs", "User name"))

      self.dbconnection_list.setSelectionBehavior(QAbstractItemView.SelectRows)
      self.dbconnection_list.setSelectionMode(QAbstractItemView.SingleSelection)

      self.dbconnection_list.setHorizontalHeaderLabels(headerLabels)
      self.dbconnection_list.horizontalHeader().show()
      self.dbconnection_list.verticalHeader().hide()

      hHeader = self.dbconnection_list.horizontalHeader()
      hHeader.sectionClicked[int].connect(self.on_sectionClicked)


   def load_dbconnection_list(self):
            
      if self.dbconnection_list.model() is not None:
         # Pulisce la tabella
         self.dbconnection_list.clearContents()
         #self.dbconnection_list.model().reset()
         self.dbconnection_list.setRowCount(0)

      self.count = 0

      row = -1
      currentRow = -1
      for lg in self.urmhsLayerGroupList.getList():
         row = row + 1
         self.insertRow(lg)
         if lg == self.urmhsLayerGroupList.currentUrmhsLayerGroup:
            currentRow = row
         
      self.OrderedCol = 0
      self.colOrderType = Qt.AscendingOrder
      self.dbconnection_list.sortItems(0, Qt.AscendingOrder)

      hHeader = self.dbconnection_list.horizontalHeader()
      hHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)
      hHeader.setStretchLastSection(True)
      
      if currentRow > -1:
         self.dbconnection_list.setCurrentCell(row, 0, QItemSelectionModel.SelectCurrent)
         for col in range(0, self.dbconnection_list.columnCount()):
            self.dbconnection_list.item(row, col).setBackground(Qt.yellow)
         self.dbconnection_list.setFocus(Qt.OtherFocusReason)         
      

   def insertRow(self, layerGroup):
      self.dbconnection_list.insertRow(self.count)
      
      uri = QgsDataSourceUri(layerGroup.dbConn.dsn)
      
      item = QTableWidgetItem(uri.host())
      item.setData(Qt.UserRole, layerGroup)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.dbconnection_list.setItem(self.count, 0, item)
      
      item = QTableWidgetItem(uri.port())
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.dbconnection_list.setItem(self.count, 1, item)
      
      item = QTableWidgetItem(uri.database())
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.dbconnection_list.setItem(self.count, 2, item)
      
      item = QTableWidgetItem(uri.username())
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.dbconnection_list.setItem(self.count, 3, item)
      
      self.count += 1


   def on_sectionClicked(self, i):
      if i != self.OrderedCol:
         self.OrderedCol = i
         self.colOrderType = Qt.AscendingOrder
      else:
         self.colOrderType = Qt.AscendingOrder if self.colOrderType == Qt.DescendingOrder else Qt.DescendingOrder
         
      self.dbconnection_list.sortItems(self.OrderedCol, self.colOrderType)
         

   def getSelectLayerGroup(self):
      sm = self.dbconnection_list.selectionModel()
      if sm.hasSelection() == False:
         return None
      selectedRow = sm.selection().indexes()[0].row()
      item = self.dbconnection_list.item(selectedRow, 0)
      return item.data(Qt.UserRole)
      
      
   def accept(self):
      layerGroup = self.getSelectLayerGroup()
      if layerGroup is None:
         QDialog.reject(self)
         return
      if layerGroup == self.urmhsLayerGroupList.currentUrmhsLayerGroup: # se si è scelto la connessione che era già corrente
         QDialog.reject(self)
         return
   
      msg = QApplication.translate("urmhs", "Are you sure you want to set <{0}> db connection as current ?")
      reply = QMessageBox.question(None, "URMHS", msg.format(layerGroup.connectionInfo()), QMessageBox.Yes | QMessageBox.No)
      if reply == QMessageBox.Yes:
         QDialog.accept(self)

   
   def reject(self):
      QDialog.reject(self)


   def onHelpButton(self):
      showHelp(QApplication.translate("Help", "Set the current DB connection"))

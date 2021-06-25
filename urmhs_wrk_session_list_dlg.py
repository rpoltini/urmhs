# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 work session list

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
from qgis.PyQt.QtWidgets import QApplication, QDialog, QMessageBox, QInputDialog, QAbstractItemView, QTableWidgetItem, QHeaderView
from qgis.core import *
from qgis.gui import *

from .urmhs_wrk_session_details_dlg import urmhsWrkSessionDetails_Dialog
from .urmhs_set_executer_dlg import urmhsSetExecuter_Dialog
from . import urmhs_wrk_session_list_ui
from . import urmhs_stack
from .urmhs_help import showHelp


#===============================================================================
# urmhsWrkSessionListModeEnum class.
#===============================================================================
class urmhsWrkSessionListModeEnum():
   SUSPEND = 0 # per sospendere una sessione di lavoro
   ACTIVATE = 1 # per attivare una sessione di lavoro
   LIST_ALL = 3 # per mostrare tutte le sessioni
   ERASE = 4 # per cancellare una sessione di lavoro
   SET_EXECUTER = 5 # per cambiare l'esecutore della sessione di lavoro


#######################################################################################
# Classe che gestisce l'interfaccia grafica per la lista delle sessioni di lavoro
class urmhsWrkSessionList_Dialog(QDialog, QObject, urmhs_wrk_session_list_ui.Ui_wrk_session_list_dialog):
   def __init__(self, parent, conn, mode):
      QDialog.__init__(self, parent)
      self.conn = conn
      self.mode = mode
      self.count = 0
      self.origCond = ''
      self.setupUi()
      self.OrderedCol = None
      self.colOrderType = None


   def setupUi(self):
      urmhs_wrk_session_list_ui.Ui_wrk_session_list_dialog.setupUi(self, self)
      
      self.wrk_session_list.setAlternatingRowColors(True)
      self.wrk_session_list.setStyleSheet("alternate-background-color: lightGray")
      self.wrk_session_list.setColumnCount(5)
      headerLabels = []
      headerLabels.append(QApplication.translate("urmhs", "Id"))
      headerLabels.append(QApplication.translate("urmhs", "Name"))
      headerLabels.append(QApplication.translate("urmhs", "Status"))
      headerLabels.append(QApplication.translate("urmhs", "Executer"))
      headerLabels.append(QApplication.translate("urmhs", "Note for executer"))

      self.wrk_session_list.setSelectionBehavior(QAbstractItemView.SelectRows)
      self.wrk_session_list.setSelectionMode(QAbstractItemView.SingleSelection)

      self.wrk_session_list.setHorizontalHeaderLabels(headerLabels)
      self.wrk_session_list.horizontalHeader().show()
      self.wrk_session_list.verticalHeader().hide()

      if self.mode == urmhsWrkSessionListModeEnum.SUSPEND:
         title = QApplication.translate("urmhs", "URMHS - Suspend a work session")
         self.origCond = 'status=' + str(urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE) + ' OR ' + \
                         'status=' + str(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE)
         self.FilterBy.addItem(QApplication.translate("urmhs", "None")) # all
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE))
                
      elif self.mode == urmhsWrkSessionListModeEnum.ACTIVATE:
         title = QApplication.translate("urmhs", "URMHS - Activate a work session")
         self.origCond = 'status=' + str(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED) + ' OR ' + \
                         'status=' + str(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE)
         self.FilterBy.addItem(QApplication.translate("urmhs", "None")) # all
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE))

      elif self.mode == urmhsWrkSessionListModeEnum.ERASE:
         title = QApplication.translate("urmhs", "URMHS - Delete a work session")
         self.origCond = 'status<>' + str(urmhs_stack.urmhsWrkSessionStatusEnum.SAVED)
         self.FilterBy.addItem(QApplication.translate("urmhs", "None")) # all
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE))

      elif self.mode == urmhsWrkSessionListModeEnum.LIST_ALL:
         title = QApplication.translate("urmhs", "URMHS - Work session list")
         self.origCond = ''
         self.FilterBy.addItem(QApplication.translate("urmhs", "None")) # all
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE))
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SAVED))

      elif self.mode == urmhsWrkSessionListModeEnum.SET_EXECUTER:
         title = QApplication.translate("urmhs", "URMHS - Change executer for a work session")
         self.origCond = 'status=' + str(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED)
         self.FilterBy.addItem(QApplication.translate("urmhs", "None")) # all
         self.FilterBy.addItem(urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED))

      self.FilterBy.setCurrentIndex(0)
      
      self.setWindowTitle(title)

      hHeader = self.wrk_session_list.horizontalHeader()
      hHeader.sectionClicked[int].connect(self.on_sectionClicked)


   def load_from_db(self, cond):
      # leggo codice session corrente
      currentwrkSessionId = urmhs_stack.get_current_wrk_session_id(self.conn)
            
      if self.wrk_session_list.model() is not None:
         # Pulisce la tabella
         self.wrk_session_list.clearContents()
         self.wrk_session_list.setRowCount(0)

      self.count = 0
      obj = urmhs_stack.urmhsWrkSessionListClass(self.conn)

      obj.load_from_db(cond, synthetic=True)
      for wrkSession in obj.wrkSessionList:
         self.insertRow(wrkSession)

      self.OrderedCol = None
      self.colOrderType = None

      hHeader = self.wrk_session_list.horizontalHeader()
      hHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)
      hHeader.setStretchLastSection(True)
      
      if currentwrkSessionId is not None:
         for row in range(0, self.wrk_session_list.rowCount()):
            item = self.wrk_session_list.item(row, 0)
            if currentwrkSessionId == item.data(Qt.DisplayRole):
               self.wrk_session_list.setCurrentCell(row, 0, QItemSelectionModel.SelectCurrent)
               for col in range(0, self.wrk_session_list.columnCount()):
                  self.wrk_session_list.item(row, col).setBackground(Qt.yellow)
               self.wrk_session_list.setFocus(Qt.OtherFocusReason)         
      

   def insertRow(self, wrkSession):
      self.wrk_session_list.insertRow(self.count)
      
      item = QTableWidgetItem()
      item.setData(Qt.DisplayRole, wrkSession.id)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_list.setItem(self.count, 0, item)
      
      item = QTableWidgetItem(wrkSession.name)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_list.setItem(self.count, 1, item)
      
      item = QTableWidgetItem(urmhs_stack.wrkSessionStatusToString(wrkSession.status))
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_list.setItem(self.count, 2, item)
      
      item = QTableWidgetItem(wrkSession.current_executer)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_list.setItem(self.count, 3, item)
      
      item = QTableWidgetItem(wrkSession.current_note)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_list.setItem(self.count, 4, item)
      
      self.count += 1


   def on_sectionClicked(self, i):
      if self.OrderedCol is None:
         self.OrderedCol = i
         self.colOrderType = Qt.AscendingOrder
      else:
         if i != self.OrderedCol:
            self.OrderedCol = i
            self.colOrderType = Qt.AscendingOrder
         else:
            self.colOrderType = Qt.AscendingOrder if self.colOrderType == Qt.DescendingOrder else Qt.DescendingOrder
         
      self.wrk_session_list.sortItems(self.OrderedCol, self.colOrderType)
         

   def getSelectWrkSessionId(self):
      sm = self.wrk_session_list.selectionModel()
      if sm.hasSelection() == False:
         return None
      selectedRow = sm.selection().indexes()[0].row()
      item = self.wrk_session_list.item(selectedRow, 0)
      return item.data(Qt.DisplayRole)
      

   def getSelectWrkSessionExecuter(self):
      sm = self.wrk_session_list.selectionModel()
      if sm.hasSelection() == False:
         return None
      selectedRow = sm.selection().indexes()[0].row()
      item = self.wrk_session_list.item(selectedRow, 3)
      return item.data(Qt.DisplayRole)

      
   def accept(self):
      sm = self.wrk_session_list.selectionModel()
      if sm.hasSelection() == False:
         QDialog.accept(self)
         return
      wrk_session_id = self.getSelectWrkSessionId()
      if wrk_session_id is None:
         return
   
      if self.mode == urmhsWrkSessionListModeEnum.ACTIVATE:
         msg = QApplication.translate("urmhs", "Are you sure you want to activate work session n.{0} (you can leave a note) ?")
         note, ok = QInputDialog.getText(None, "URMHS", msg.format(str(wrk_session_id)))         
         
         if ok:         
            if urmhs_stack.wrk_session_set_active_status(self.conn, wrk_session_id, note) == True:
               QDialog.accept(self)
               
      elif self.mode == urmhsWrkSessionListModeEnum.ERASE:
         msg = QApplication.translate("urmhs", "Are you sure you want to delete work session n.{0} ?")
         reply = QMessageBox.question(None, "URMHS", msg.format(str(wrk_session_id)), QMessageBox.Yes | QMessageBox.No)
         if reply == QMessageBox.Yes:         
            if urmhs_stack.wrk_session_delete(self.conn, wrk_session_id) == True:
               QDialog.accept(self)
               
      elif self.mode == urmhsWrkSessionListModeEnum.SET_EXECUTER:
         dlg = urmhsSetExecuter_Dialog(self, self.conn, self.getSelectWrkSessionExecuter())
         if dlg.exec_() == QDialog.Accepted:
            res = urmhs_stack.wrk_session_set_executer(self.conn, wrk_session_id, \
                                                       dlg.user_comboBox.currentText(), \
                                                       dlg.note_plainTextEdit.toPlainText()) == True
            if res == True:
               QDialog.accept(self)
               
      else:
         QDialog.accept(self)

   
   def reject(self):
      QDialog.reject(self)


   def onHelpButton(self):
      if self.mode == urmhsWrkSessionListModeEnum.SUSPEND:
         showHelp(QApplication.translate("Help", "Suspend a work session"))
      elif self.mode == urmhsWrkSessionListModeEnum.ACTIVATE:
         showHelp(QApplication.translate("Help", "Activate a work session"))
      elif self.mode == urmhsWrkSessionListModeEnum.ERASE:
         showHelp(QApplication.translate("Help", "Erase a work session"))


   def onFilterChanged(self, index):
      cond = self.origCond
      if self.FilterBy.itemText(index) == urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE):
         filterCond = "status=" + str(urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE)
      elif self.FilterBy.itemText(index) == urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE):
         filterCond = "status=" + str(urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE)
      elif self.FilterBy.itemText(index) == urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SAVED):
         filterCond = "status=" + str(urmhs_stack.urmhsWrkSessionStatusEnum.SAVED)
      elif self.FilterBy.itemText(index) == urmhs_stack.wrkSessionStatusToString(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED):
         filterCond = "status=" + str(urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED)
      else:
         filterCond = ""
         
      if len(filterCond) > 0:
         filterCond = "(" + filterCond + ")"
         
      if len(cond) > 0:
         if len(filterCond) > 0:
            cond = cond + " AND " + filterCond
      else:
         cond = filterCond
      
      self.load_from_db(cond)
   
   
   def onDetailsButton(self):
      wrk_session_id = self.getSelectWrkSessionId()
      if wrk_session_id is None:
         return

      obj = urmhs_stack.urmhsWrkSessionListClass(self.conn)
      obj.load_from_db("id=" + str(wrk_session_id), synthetic=False)
      if len(obj.wrkSessionList) == 1:
         dlg = urmhsWrkSessionDetails_Dialog(None, obj.wrkSessionList[0])
         dlg.exec_()

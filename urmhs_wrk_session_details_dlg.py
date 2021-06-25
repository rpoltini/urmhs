# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 work session detail

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
from qgis.PyQt.QtWidgets import QApplication, QDialog, QAbstractItemView, QTableWidgetItem, QHeaderView, QGraphicsScene
from qgis.core import *

from . import urmhs_wrk_session_details_ui
from . import urmhs_stack
from .urmhs_help import showHelp


#######################################################################################
# Classe che gestisce l'interfaccia grafica della funzione di creazione di una sessione di lavoro
class urmhsWrkSessionDetails_Dialog(QDialog, QObject, urmhs_wrk_session_details_ui.Ui_wrk_session_details_dialog):
   def __init__(self, parent, wrk_session):
      QDialog.__init__(self, parent)      

      self.setupUi(self)
      self.wrk_session_history_list_setupUi()
      
      self.wrk_session_id.setText(str(wrk_session.id))
      self.wrk_session_name.setText(wrk_session.name)
      self.wrk_session_status.setText(urmhs_stack.wrkSessionStatusToString(wrk_session.status))
      self.wrk_session_descr.setText(wrk_session.descr)
      self.created_by.setText(wrk_session.created_by)
      if wrk_session.creation_date is not None:
         self.creation_date.setText(wrk_session.creation_date.strftime('%c')) # Locale’s appropriate date and time representation
      self.saved_by.setText(wrk_session.saved_by)
      if wrk_session.save_date is not None:
         self.save_date.setText(wrk_session.save_date.strftime('%c')) # Locale’s appropriate date and time representation
         
      if wrk_session.current_image is not None:
         self.lbl_image.setPixmap(wrk_session.current_image)
      
      wrk_session.load_history_from_db()
      self.count = 0
      for historyItem in wrk_session.historyList:
         self.insertRow(historyItem)
         
      hHeader = self.wrk_session_history_list.horizontalHeader()
      hHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)
      hHeader.setSectionResizeMode(1, QHeaderView.ResizeToContents)
      hHeader.setStretchLastSection(True)


   def wrk_session_history_list_setupUi(self):
      self.wrk_session_history_list.setAlternatingRowColors(True)
      self.wrk_session_history_list.setStyleSheet("alternate-background-color: lightGray")
      self.wrk_session_history_list.setColumnCount(5)
      headerLabels = []
      headerLabels.append(QApplication.translate("urmhs", "Author"))
      headerLabels.append(QApplication.translate("urmhs", "Date"))
      headerLabels.append(QApplication.translate("urmhs", "Status"))
      headerLabels.append(QApplication.translate("urmhs", "Executer"))
      headerLabels.append(QApplication.translate("urmhs", "Note for executer"))

      self.wrk_session_history_list.setSelectionBehavior(QAbstractItemView.SelectRows)
      self.wrk_session_history_list.setSelectionMode(QAbstractItemView.SingleSelection)

      self.wrk_session_history_list.setHorizontalHeaderLabels(headerLabels)
      self.wrk_session_history_list.horizontalHeader().show()
      self.wrk_session_history_list.verticalHeader().hide()


   def insertRow(self, historyItem):
      self.wrk_session_history_list.insertRow(self.count)
      
      item = QTableWidgetItem()
      item.setData(Qt.DisplayRole, historyItem.author)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_history_list.setItem(self.count, 0, item)
      
      item = QTableWidgetItem(historyItem.date.strftime('%c')) # Locale’s appropriate date and time representation)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_history_list.setItem(self.count, 1, item)
      
      item = QTableWidgetItem(urmhs_stack.wrkSessionStatusToString(historyItem.status))
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_history_list.setItem(self.count, 2, item)
      
      item = QTableWidgetItem(historyItem.executer)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_history_list.setItem(self.count, 3, item)
      
      item = QTableWidgetItem(historyItem.note)
      item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
      self.wrk_session_history_list.setItem(self.count, 4, item)
      
      self.count += 1


   def accept(self):
      QDialog.accept(self)

   
   def onHelpButton(self):
      showHelp(QApplication.translate("Help", "Work session detail"))

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 work session creation

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
from qgis.PyQt.QtWidgets import QApplication, QDialog
from qgis.core import *

from . import urmhs_wrk_session_create_ui
from . import urmhs_users
from . import urmhs_stack
from .urmhs_help import showHelp


#######################################################################################
# Classe che gestisce l'interfaccia grafica della funzione di creazione di una sessione di lavoro
class urmhsCreateWrkSession_Dialog(QDialog, QObject, urmhs_wrk_session_create_ui.Ui_wrk_session_create_dialog):
   def __init__(self, parent, conn):
      QDialog.__init__(self, parent)      
      self.conn = conn

      self.setupUi(self)
      self.next_wrk_session_id = urmhs_stack.get_next_wrk_session_id(self.conn)
      
      wrk_session_name = QApplication.translate("urmhs", "Work session")
      self.wrk_session_name.setText(wrk_session_name + " " + str(self.next_wrk_session_id))
      # ricavo l'utente corrente
      uri = QgsDataSourceUri(self.conn.dsn)
      current_login = uri.username()
      userList = urmhs_users.urmhsUserListClass(self.conn)
      i = 0
      for user in userList.userList:
         self.wrk_session_executor.addItem(user.login)
         if user.login == current_login:
            self.wrk_session_executor.setCurrentIndex(i)
         i = i + 1
      

   def accept(self):
      id = urmhs_stack.wrk_session_create(self.conn, self.wrk_session_name.text(), \
                                          self.wrk_session_descr.toPlainText(), \
                                          self.wrk_session_executor.currentText(),
                                          self.wrk_session_note.toPlainText(),
                                          self.next_wrk_session_id)
      if id > 0:
         QDialog.accept(self)

   
   def reject(self):
      QDialog.reject(self)


   def onHelpButton(self):
      showHelp(QApplication.translate("Help", "Work session creation"))

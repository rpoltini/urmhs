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

from . import urmhs_set_executer_ui
from . import urmhs_users
from . import urmhs_stack
from .urmhs_help import showHelp


#######################################################################################
# Classe che gestisce l'interfaccia grafica della funzione di cambio di esecutore di una sessione di lavoro
class urmhsSetExecuter_Dialog(QDialog, QObject, urmhs_set_executer_ui.Ui_SetExecuterDialog):
   def __init__(self, parent, conn, WrkSessionExecuter):
      QDialog.__init__(self, parent)
      self.conn = conn

      self.setupUi(self)
      current_login = urmhs_users.quote_literal(self.conn, WrkSessionExecuter)
      
      userList = urmhs_users.urmhsUserListClass(self.conn)
      userList.load_from_db("login <> " + current_login) 
      i = 0
      for user in userList.userList:
         self.user_comboBox.addItem(user.login)
         i = i + 1
      

   def accept(self):
      if (self.user_comboBox.currentText() != ""):
         QDialog.accept(self)

   
   def reject(self):
      QDialog.reject(self)


   def onHelpButton(self):
      showHelp(QApplication.translate("Help", "Work session creation"))

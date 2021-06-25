# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 user details

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
from qgis.PyQt.QtWidgets import QApplication, QDialog, QMessageBox
from qgis.core import *

from . import urmhs_user_ui
from . import urmhs_users
from .urmhs_help import showHelp


#===============================================================================
# urmhsUserDlgModeEnum class.
#===============================================================================
class urmhsUserDlgModeEnum():
   ADD = 0 # per aggiungere un nuovo utente
   UPD = 1 # per modificare un utente
   DEL = 3 # per cancellare un utente


#######################################################################################
# Classe che gestisce l'interfaccia grafica della funzione di creazione di una sessione di lavoro
class urmhsUser_Dialog(QDialog, QObject, urmhs_user_ui.Ui_user_dialog):
   def __init__(self, parent, conn, user = None, mode = urmhsUserDlgModeEnum.ADD):
      QDialog.__init__(self, parent)
      self.conn = conn
      self.mode = mode

      self.setupUi(self)

      if self.mode == urmhsUserDlgModeEnum.ADD:
         self.user = urmhs_users.urmhsUserClass()
      else:
         self.user = user
         self.login.setText(str(user.login))
         
         if self.user.isSuperUser:
            self.superuser.setCheckState(Qt.Checked)
         else:
            self.superuser.setCheckState(Qt.Unchecked)
            
         if self.user.canSave or self.user.isSuperUser:
            self.save.setCheckState(Qt.Checked)
            self.save.setEnabled(False)
         else:
            self.save.setCheckState(Qt.Unchecked)

         self.security_question.setText(self.user.security_question)
         self.security_answer.setText("********")
         
         if self.mode == urmhsUserDlgModeEnum.DEL:
            self.login.setEnabled(False)
            self.superuser.setEnabled(False)
            self.save.setEnabled(False)
            self.security_question.setEnabled(False)
            self.security_answer.setEnabled(False)


   def accept(self):
      oldUserLogin = self.user.login
      self.user.login = self.login.text()

      if self.superuser.checkState() == Qt.Checked:
         self.user.isSuperUser = True
      else:
         self.user.isSuperUser = False

      if self.save.checkState() == Qt.Checked or self.user.isSuperUser:
         self.user.canSave = True
      else:
         self.user.canSave = False
      
      self.user.security_question = self.security_question.text()
      
      self.security_answer.text()
      
      obj = urmhs_users.urmhsUserListClass(self.conn)
      if self.mode == urmhsUserDlgModeEnum.ADD:
         if obj.add_user_to_db(self.user, self.security_answer.text()) == True:
            QDialog.accept(self)         
      elif self.mode == urmhsUserDlgModeEnum.UPD:
         if obj.upd_user_to_db(oldUserLogin, self.user) == True and \
            obj.upd_user_security_to_db(self.user.login, self.user.security_question, \
                                        self.security_answer.text()) == True:
            QDialog.accept(self)
      elif self.mode == urmhsUserDlgModeEnum.DEL:
         msg = QApplication.translate("urmhs", "Are you sure you want to delete the {0} user ?").format(self.user.login)
         reply = QMessageBox.question(None, "URMHS", msg, QMessageBox.Yes | QMessageBox.No)
         if reply == QMessageBox.Yes:
            if obj.del_user_to_db(self.user.login) == True:
               QDialog.accept(self)
         
   
   def onHelpButton(self):
      showHelp(QApplication.translate("Help", "User detail"))


   def onSuperUser(self):
      if self.superuser.checkState() == Qt.Checked:
         self.save.setEnabled(False)
         self.save.setCheckState(Qt.Checked)
      else:
         self.save.setEnabled(True)
      

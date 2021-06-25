from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QApplication, QDialog

from . import urmhs_user_confirm_ui
from . import urmhs_users
from .urmhs_help import showHelp


#######################################################################################
# Classe che gestisce l'interfaccia grafica per la lista delle sessioni di lavoro
class urmhsUserConfirm_Dialog(QDialog, QObject, urmhs_user_confirm_ui.Ui_user_confirm_dialog):
   def __init__(self, parent, conn):
      QDialog.__init__(self, parent)
      self.conn = conn
      self.setupUi(self)
      # leggo dettagli dell'utente corrente
      currUser = urmhs_users.get_current_user_details(self.conn)
      if currUser is None:
         return
      self.current_login.setText(currUser.login)
      self.security_question.setText(currUser.securityQuestion)
      self.security_answer.setFocus(Qt.OtherFocusReason)


   def accept(self):
      if urmhs_users.force_current_inet_client_addr(self.conn, self.security_answer.text()) == True:
         QDialog.accept(self)


   def reject(self):
      QDialog.reject(self)


   def onHelpButton(self):
      showHelp(QApplication.translate("Help", "User confirmation"))

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

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


# Import the PyQt and QGIS libraries

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QApplication, QDialog, QMessageBox, QInputDialog, QAction, QMenu, QToolButton, QLabel
from qgis.core import *
from qgis.gui import *
import locale

# Initialize Qt resources from file urmhs_rc.py
from .urmhs_rc import *

import os.path

from . import urmhs_users
from . import urmhs_stack
from .urmhs_layer_group import urmhsLayerGroupListClass, urmhsFunctionalityTypeEnum
from .urmhs_wrk_session_create_dlg import urmhsCreateWrkSession_Dialog
from .urmhs_wrk_session_list_dlg import urmhsWrkSessionList_Dialog, urmhsWrkSessionListModeEnum
from .urmhs_user_confirm_dlg import urmhsUserConfirm_Dialog
from .urmhs_enable_stack_dlg import urmhsEnableStackModeEnum, urmhsEnableStack_Dialog
from .urmhs_enable_history_dlg import urmhsEnableHistoryModeEnum, urmhsEnableHistory_Dialog
from .urmhs_set_history_date_dlg import urmhsSetHistoryDate_Dialog
from .urmhs_user_list_dlg import urmhsUserList_Dialog
from .urmhs_dbconnection_list_dlg import urmhsDBConnectionList_Dialog


class urmhs(QObject):
   """
   Classe plugin di urmhs
   """

   
   #============================================================================
   # __init__
   #============================================================================
   def __init__(self, iface):
      
      QObject.__init__(self)      
            
      # Save reference to the QGIS interface
      self.iface = iface
      
      # initialize plugin directory
      self.plugin_dir = os.path.dirname(__file__)

      self.canvas = self.iface.mapCanvas()

      self.urmhsLayerGroupList = urmhsLayerGroupListClass(self)
      self.setHistoryDate_Dialog = None
      
      # initialize locale
      userLocaleList = QSettings().value("locale/userLocale").split("_")
      language = userLocaleList[0]
      region = userLocaleList[1] if len(userLocaleList) > 1 else ""
      # provo a caricare la lingua e la regione selezionate
      if self.__initLocalization(language + "_" + region) == False:
         # provo a caricare la lingua
         self.__initLocalization(language)
         
      locale.setlocale(locale.LC_ALL, '')
         

   #============================================================================
   # __del__
   #============================================================================
   def __del__(self):
      pass


   #============================================================================
   # unload
   #============================================================================
   def unload(self):
      if self.urmhsLayerGroupList.currentUrmhsLayerGroup is not None:
         QSettings().setValue("/urmhs/lastUsedProjectName", QgsProject.instance().baseName())         
         QSettings().setValue("/urmhs/lastUsedConnectionInfo", self.urmhsLayerGroupList.currentUrmhsLayerGroup.connectionInfo())
      
      QgsProject.instance().layerWasAdded.disconnect(self.add_layer)
      QgsProject.instance().layerWillBeRemoved.disconnect(self.remove_layer)
      self.iface.projectRead.disconnect(self.project_read)

      # Remove the plugin menu item and icon
      self.iface.removeToolBarIcon(self.help_action)
      self.iface.removePluginVectorMenu("URMHS", self.help_action)
      # remove toolbars and menubars
      if self.usrToolBar is not None:
         del self.usrToolBar
      if self.adminToolBar is not None:
         del self.adminToolBar

      if self.menu is not None:
         del self.menu
      if self.workSessionMenu is not None:
         del self.workSessionMenu
      if self.enableStackMenu is not None:
         del self.enableStackMenu
      if self.enableHistoryMenu is not None:
         del self.enableHistoryMenu

      if self.setHistoryDate_Dialog is not None:
         self.iface.removeDockWidget(self.setHistoryDate_Dialog)
         del self.setHistoryDate_Dialog
      
      del self.urmhsLayerGroupList # svuoto la lista


   #============================================================================
   # INIZIO - Gestione ACTION (da chiamare prima di creare MENU e TOOLBAR) 
   #============================================================================
   def initActions(self):
      # Creo le azioni e le collego ai comandi
      
      # help
      self.help_action = QAction(QIcon(":/plugins/urmhs/icons/help.png"), \
                                QApplication.translate("urmhs", "Help"),
                                self.iface.mainWindow())
      self.help_action.triggered.connect(self.doHelp)
      
      # undo
      self.undo_action = QAction(QIcon(":/plugins/urmhs/icons/undo.png"), \
                                 QApplication.translate("urmhs", "Undo"), \
                                 self.iface.mainWindow())
      self.undo_action.triggered.connect(self.doUndo)

      # nUndo
      self.nUndo_action = QAction(QIcon(":/plugins/urmhs/icons/n_undo.png"), \
                                 QApplication.translate("urmhs", "Undo n operations"), \
                                 self.iface.mainWindow())
      self.nUndo_action.triggered.connect(self.doNUndo)

      # redo
      self.redo_action = QAction(QIcon(":/plugins/urmhs/icons/redo.png"), \
                                 QApplication.translate("urmhs", "Redo"), \
                                 self.iface.mainWindow())
      self.redo_action.triggered.connect(self.doRedo)

      # nRedo
      self.nRedo_action = QAction(QIcon(":/plugins/urmhs/icons/n_redo.png"), \
                                 QApplication.translate("urmhs", "Redo n operations"), \
                                 self.iface.mainWindow())
      self.nRedo_action.triggered.connect(self.doNRedo)

      # undoBeginGroup
      self.undoBeginGroup_action = QAction(QIcon(":/plugins/urmhs/icons/undo_begin_group.png"), \
                                 QApplication.translate("urmhs", "Begin a group of operations"), \
                                 self.iface.mainWindow())
      self.undoBeginGroup_action.triggered.connect(self.doUndoBeginGroup)

      # undoEndGroup
      self.undoEndGroup_action = QAction(QIcon(":/plugins/urmhs/icons/undo_end_group.png"), \
                                 QApplication.translate("urmhs", "End a group of operations"), \
                                 self.iface.mainWindow())
      self.undoEndGroup_action.triggered.connect(self.doUndoEndGroup)

      # undoInsertBookmark
      self.undoInsertBookmark_action = QAction(QIcon(":/plugins/urmhs/icons/undo_insert_bookmark.png"), \
                                 QApplication.translate("urmhs", "Insert a bookmark"), \
                                 self.iface.mainWindow())
      self.undoInsertBookmark_action.triggered.connect(self.doUndoInsertBookmark)

      # undoBookmark
      self.undoBookmark_action = QAction(QIcon(":/plugins/urmhs/icons/undo_bookmark.png"), \
                                 QApplication.translate("urmhs", "Undo to a bookmark"), \
                                 self.iface.mainWindow())
      self.undoBookmark_action.triggered.connect(self.doUndoBookmark)

      # redoBookmark
      self.redoBookmark_action = QAction(QIcon(":/plugins/urmhs/icons/redo_bookmark.png"), \
                                 QApplication.translate("urmhs", "Redo to a bookmark"), \
                                 self.iface.mainWindow())
      self.redoBookmark_action.triggered.connect(self.doRedoBookmark)


      # SESSIONI DI LAVORO
      # ------------------
      
      # workSessionCreate
      self.workSessionCreate_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_create.png"), \
                                              QApplication.translate("urmhs", "Create a new work session"), \
                                              self.iface.mainWindow())
      self.workSessionCreate_action.triggered.connect(self.doWorkSessionCreate)

      # workSessionSave
      self.workSessionSave_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_save.png"), \
                                            QApplication.translate("urmhs", "Save the current active work session"), \
                                            self.iface.mainWindow())
      self.workSessionSave_action.triggered.connect(self.doCurrentWorkSessionSave)

      # workSessionDel
      self.workSessionDel_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_del.png"), \
                                           QApplication.translate("urmhs", "Delete a work session"), \
                                           self.iface.mainWindow())
      self.workSessionDel_action.triggered.connect(self.doWorkSessionDel)

      # workSessionActivate
      self.workSessionActivate_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_activate.png"), \
                                                QApplication.translate("urmhs", "Activate a work session"), \
                                                self.iface.mainWindow())
      self.workSessionActivate_action.triggered.connect(self.doWorkSessionActivate)

      # workSessionSuspend
      self.workSessionSuspend_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_suspend.png"), \
                                               QApplication.translate("urmhs", "Suspend the current work session"), \
                                               self.iface.mainWindow())
      self.workSessionSuspend_action.triggered.connect(self.doCurrentWorkSessionSuspend)

      # workSessionList
      self.workSessionList_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_list.png"), \
                                               QApplication.translate("urmhs", "List all work sessions"), \
                                               self.iface.mainWindow())
      self.workSessionList_action.triggered.connect(self.doWorkSessionList)
      # workSessionChangeExecuter
      self.workSessionChangeExecuter_action = QAction(QIcon(":/plugins/urmhs/icons/wrk_session_chage_executer.png"), \
                                               QApplication.translate("urmhs", "Change work session executor"), \
                                               self.iface.mainWindow())
      self.workSessionChangeExecuter_action.triggered.connect(self.doWorkSessionSetExecuter)
      
      # STACK
      # -----
      
      # enableStack
      self.enableStack_action = QAction(QIcon(":/plugins/urmhs/icons/enable_stack.png"), \
                                        QApplication.translate("urmhs", "Enable stack to layers"), \
                                        self.iface.mainWindow())
      self.enableStack_action.triggered.connect(self.doEnableStack)
      
      # disableStack
      self.disableStack_action = QAction(QIcon(":/plugins/urmhs/icons/disable_stack.png"), \
                                         QApplication.translate("urmhs", "Disable stack to layers"), \
                                         self.iface.mainWindow())
      self.disableStack_action.triggered.connect(self.doDisableStack)

      # HISTORY
      # -------

      # setHistoryDate
      self.setHistoryDate_action = QAction(QIcon(":/plugins/urmhs/icons/set_history_date.png"), \
                                           QApplication.translate("urmhs", "Set history date"), \
                                           self.iface.mainWindow())
      self.setHistoryDate_action.triggered.connect(self.doSetHistoryDate)

      # enableHistory
      self.enableHistory_action = QAction(QIcon(":/plugins/urmhs/icons/enable_history.png"), \
                                           QApplication.translate("urmhs", "Enable history to layers"), \
                                           self.iface.mainWindow())
      self.enableHistory_action.triggered.connect(self.doEnableHistory)

      # disableHistory
      self.disableHistory_action = QAction(QIcon(":/plugins/urmhs/icons/disable_history.png"), \
                                           QApplication.translate("urmhs", "Disable history to layers"), \
                                           self.iface.mainWindow())
      self.disableHistory_action.triggered.connect(self.doDisableHistory)

      # UTENTI
      # ------
      
      # userManagement
      self.userManagement_action = QAction(QIcon(":/plugins/urmhs/icons/user_management.png"), \
                                           QApplication.translate("urmhs", "User management"), \
                                           self.iface.mainWindow())
      self.userManagement_action.triggered.connect(self.doUserManagement)

      # UTILITA'
      # --------
      
      # userConfirm
      self.userConfirm_action = QAction(QIcon(":/plugins/urmhs/icons/user_confirm.png"), \
                                           QApplication.translate("urmhs", "Confirm the user identity"), \
                                           self.iface.mainWindow())
      self.userConfirm_action.triggered.connect(self.doUserConfirm)

      # setCurrentDBConnection
      self.setCurrentDBConnection_action = QAction(QIcon(":/plugins/urmhs/icons/set_current_dbconnection.png"), \
                                           QApplication.translate("urmhs", "Set current DB connection"), \
                                           self.iface.mainWindow())
      self.setCurrentDBConnection_action.triggered.connect(self.doSetCurrentDBConnection)


   def initGui(self):
      # creo tutte le azioni e le collego ai comandi
      self.initActions()
      self.addMenu()
      self.addToolBar()
      
      # se ci sono più connessioni possibili prendo l'ultima usata
      if len(self.urmhsLayerGroupList.getList()) > 1:
         if QSettings().value("/urmhs/lastUsedProjectName", "") == QgsProject.instance().baseName():
            self.urmhsLayerGroupList.setCurrentDbConn(QSettings().value("/urmhs/lastUsedConnectionInfo", ""))
            
      QgsProject.instance().layerWasAdded.connect(self.add_layer)
      QgsProject.instance().layerWillBeRemoved.connect(self.remove_layer)
      self.iface.projectRead.connect(self.project_read)

      self.urmhsLayerGroupList.init()
            
      self.enableActions()
      self.refreshWrkSessionLbl()


   def addMenu(self):
      # Add menu
      self.menu = QMenu("URMHS")
      self.menu.addAction(self.help_action)
      
      self.menu.addSeparator()

      # crea il menu Undo
      self.undoMenu = self.createUndoMenu()
      self.menu.addMenu(self.undoMenu)
      
      # crea il menu Redo
      self.redoMenu = self.createRedoMenu()
      self.menu.addMenu(self.redoMenu)
      
      # crea il menu Work session
      self.workSessionMenu = self.createWorkSessionMenu()
      self.menu.addMenu(self.workSessionMenu)
 
      self.menu.addSeparator()
      
      # crea il menu enableStack
      self.enableStackMenu = self.createEnableStackMenu()
      self.menu.addMenu(self.enableStackMenu)

      self.menu.addSeparator()
      
      self.menu.addAction(self.setHistoryDate_action)

      # crea il menu History
      self.enableHistoryMenu = self.createHistoryMenu()
      self.menu.addMenu(self.enableHistoryMenu)

      # crea il menu User
      self.userMenu = self.createUserMenu()
      self.menu.addMenu(self.userMenu)
      
      # crea il menu Utility      
      self.utilityMenu = self.createUtilityMenu()
      self.menu.addMenu(self.utilityMenu)

      # aggiunge il menu al menu vector di QGIS
      self.iface.vectorMenu().addMenu(self.menu)


   def createUndoMenu(self):
      # menu undo\redo
      undoMenu = QMenu(QApplication.translate("urmhs", "Undo"))
      undoMenu.addAction(self.undo_action)
      undoMenu.addAction(self.nUndo_action)
      undoMenu.addAction(self.undoBeginGroup_action)
      undoMenu.addAction(self.undoEndGroup_action)
      undoMenu.addAction(self.undoInsertBookmark_action)
      undoMenu.addAction(self.undoBookmark_action)
      
      return undoMenu


   def createRedoMenu(self):
      # menu redo
      redoMenu = QMenu(QApplication.translate("urmhs", "Redo"))
      redoMenu.addAction(self.redo_action)
      redoMenu.addAction(self.nRedo_action)
      redoMenu.addAction(self.redoBookmark_action)
      
      return redoMenu
      

   def createWorkSessionMenu(self):
      # menu work session
      workSessionMenu = QMenu(QApplication.translate("urmhs", "Work session management"))
      workSessionMenu.addAction(self.workSessionCreate_action)
      workSessionMenu.addAction(self.workSessionSave_action)
      workSessionMenu.addAction(self.workSessionDel_action)
      workSessionMenu.addAction(self.workSessionActivate_action)
      workSessionMenu.addAction(self.workSessionSuspend_action)
      workSessionMenu.addAction(self.workSessionList_action)
      workSessionMenu.addAction(self.workSessionChangeExecuter_action)
      
      return workSessionMenu


   def createEnableStackMenu(self):
      # menu enable/disable stack
      enableStackMenu = QMenu(QApplication.translate("urmhs", "Stack management"))
      enableStackMenu.addAction(self.enableStack_action)
      enableStackMenu.addAction(self.disableStack_action)
      return enableStackMenu


   def createHistoryMenu(self):
      # menu enable/disable stack
      enableHistoryMenu = QMenu(QApplication.translate("urmhs", "History management"))
      enableHistoryMenu.addAction(self.enableHistory_action)
      enableHistoryMenu.addAction(self.disableHistory_action)
      return enableHistoryMenu


   def createUserMenu(self):
      # menu user management
      userMenu = QMenu(QApplication.translate("urmhs", "User management"))
      userMenu.addAction(self.userManagement_action)
      return userMenu


   def createUtilityMenu(self):
      # menu user management
      utilityMenu = QMenu(QApplication.translate("urmhs", "Utility"))
      utilityMenu.addAction(self.userConfirm_action)
      utilityMenu.addAction(self.setCurrentDBConnection_action)
      return utilityMenu


   def addToolBar(self):
      # aggiunge una toolbar
      self.usrToolBar = self.iface.addToolBar("urmhs_usrToolBar")
      self.usrToolBar.setObjectName("urmhs_usrToolBar")

      self.usrToolBar.addAction(self.help_action)
      
      # Undo
      self.undoToolButton = self.createUndoToolButton()
      self.usrToolBar.addWidget(self.undoToolButton)

      # Redo
      self.redoToolButton = self.createRedoToolButton()
      self.usrToolBar.addWidget(self.redoToolButton)

      # Label for active worksession name
      self.wrkSessionLbl = QLabel(self.usrToolBar)
      self.usrToolBar.addWidget(self.wrkSessionLbl)
      
      # Work session
      self.workSessionToolButton = self.createWorkSessionToolButton()
      self.usrToolBar.addWidget(self.workSessionToolButton)
      
      self.usrToolBar.addSeparator()
      
      self.usrToolBar.addAction(self.setHistoryDate_action)

      self.usrToolBar.addSeparator()
      
      # aggiunge una toolbar
      self.adminToolBar = self.iface.addToolBar("urmhs_adminToolBar")
      self.adminToolBar.setObjectName("urmhs_adminToolBar")

      # enable stack
      self.enableStackToolButton = self.createEnableStackToolButton()
      self.adminToolBar.addWidget(self.enableStackToolButton)
      
      # enable history
      self.enableHistoryToolButton = self.createEnableHistoryToolButton()
      self.adminToolBar.addWidget(self.enableHistoryToolButton)

      # user management
      self.userToolButton = self.createUserToolButton()
      self.adminToolBar.addWidget(self.userToolButton)

      # aggiunge una toolbar
      self.utilityToolBar = self.iface.addToolBar("urmhs_utilityToolBar")
      self.utilityToolBar.setObjectName("urmhs_utilityToolBar")

      # Utility
      self.utilityToolButton = self.createUtilityToolButton()
      self.utilityToolBar.addWidget(self.utilityToolButton)
      

   def createUndoToolButton(self):
      undoToolButton = QToolButton(self.usrToolBar)
      undoToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      undoToolButton.setMenu(self.undoMenu)
      undoToolButton.setDefaultAction(self.undoMenu.actions()[0]) # prima voce di menu
      undoToolButton.triggered.connect(self.undoToolButtonTriggered)
      return undoToolButton
   def undoToolButtonTriggered(self, action):
      if action.isEnabled():
         self.undoToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.undoToolButton)


   def createRedoToolButton(self):
      redoToolButton = QToolButton(self.usrToolBar)
      redoToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      redoToolButton.setMenu(self.redoMenu)
      redoToolButton.setDefaultAction(self.redoMenu.actions()[0]) # prima voce di menu
      redoToolButton.triggered.connect(self.redoToolButtonTriggered)
      return redoToolButton
   def redoToolButtonTriggered(self, action):
      if action.isEnabled():
         self.redoToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.redoToolButton)


   def createWorkSessionToolButton(self):
      workSessionToolButton = QToolButton(self.usrToolBar)
      workSessionToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      workSessionToolButton.setMenu(self.workSessionMenu)
      workSessionToolButton.setDefaultAction(self.workSessionMenu.actions()[0]) # prima voce di menu
      workSessionToolButton.triggered.connect(self.workSessionToolButtonTriggered)
      return workSessionToolButton
   def workSessionToolButtonTriggered(self, action):
      if action.isEnabled():
         self.workSessionToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.workSessionToolButton)


   def createEnableStackToolButton(self):
      enableStackToolButton = QToolButton(self.adminToolBar)
      enableStackToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      enableStackToolButton.setMenu(self.enableStackMenu)
      enableStackToolButton.setDefaultAction(self.enableStackMenu.actions()[0]) # prima voce di menu
      enableStackToolButton.triggered.connect(self.enableStackToolButtonTriggered)
      return enableStackToolButton
   def enableStackToolButtonTriggered(self, action):
      if action.isEnabled():
         self.enableStackToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.enableStackToolButton)


   def createEnableHistoryToolButton(self):
      enableHistoryToolButton = QToolButton(self.adminToolBar)
      enableHistoryToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      enableHistoryToolButton.setMenu(self.enableHistoryMenu)
      enableHistoryToolButton.setDefaultAction(self.enableHistoryMenu.actions()[0]) # prima voce di menu
      enableHistoryToolButton.triggered.connect(self.enableHistoryToolButtonTriggered)
      return enableHistoryToolButton
   def enableHistoryToolButtonTriggered(self, action):
      if action.isEnabled():
         self.enableHistoryToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.enableHistoryToolButton)


   def createUserToolButton(self):
      userToolButton = QToolButton(self.adminToolBar)
      userToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      userToolButton.setMenu(self.userMenu)
      userToolButton.setDefaultAction(self.userMenu.actions()[0]) # prima voce di menu
      userToolButton.triggered.connect(self.userToolButtonTriggered)
      return userToolButton
   def userToolButtonTriggered(self, action):
      if action.isEnabled():
         self.userToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.userToolButton)


   def createUtilityToolButton(self):
      utilityToolButton = QToolButton(self.utilityToolBar)
      utilityToolButton.setPopupMode(QToolButton.MenuButtonPopup)
      utilityToolButton.setMenu(self.utilityMenu)
      utilityToolButton.setDefaultAction(self.utilityMenu.actions()[0]) # prima voce di menu
      utilityToolButton.triggered.connect(self.utilityToolButtonTriggered)
      return utilityToolButton
   def utilityToolButtonTriggered(self, action):
      if action.isEnabled():
         self.utilityToolButton.setDefaultAction(action)
      else:
         self.setFirstEnabledDefaultAction(self.utilityToolButton)


   def setFirstEnabledDefaultAction(self, tButton):
      #if tButton.defaultAction().isEnabled():
      #   return
      for action in tButton.menu().actions():
         if action.isEnabled():
            tButton.setDefaultAction(action)
            break
   

   def refreshWrkSessionLbl(self):
      msg = None
      conn = self.getCurrentDbConn(urmhsFunctionalityTypeEnum.STACK)
      if conn is not None:
         # leggo codice sessione corrente
         currentWrkSession = urmhs_stack.get_current_wrk_session_details(conn)
         if currentWrkSession is not None and \
            currentWrkSession.status == urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE:
            msg = QApplication.translate("urmhs", "Current active work session: n.{0}, named {1}, created by {2} on {3}")
            msg = msg.format(str(currentWrkSession.id), currentWrkSession.name, \
                             currentWrkSession.created_by, currentWrkSession.creation_date.strftime('%c'))
   
      if msg is None:
         msg = QApplication.translate("urmhs", "No current active work session")
         
      self.wrkSessionLbl.setText(msg)


   #============================================================================
   # __initLocalization
   #============================================================================
   # inizializza la localizzazione delle traduzioni e dell'help in linea
   def __initLocalization(self, locale):     
      localePath = os.path.join(self.plugin_dir, 'i18n', 'urmhs_{}.qm'.format(locale))

      if os.path.exists(localePath):
         self.translator = QTranslator()
         self.translator.load(localePath)
         if qVersion() > '4.3.3':
            QCoreApplication.installTranslator(self.translator)
         return True
      else:
         return False


   def add_layer(self, layer):
      if self.urmhsLayerGroupList.add_layer(layer):
         self.enableActions()
      
      
   def remove_layer(self, layerId):
      layer = QgsProject.instance().mapLayers()[layerId]
      if self.urmhsLayerGroupList.remove_layer(layer):
         self.enableActions()
   

   def project_read(self):
      self.urmhsLayerGroupList.init()
      n = len(self.urmhsLayerGroupList.getList())
      if n > 1:  # se ci sono più connessioni possibili prendo l'ultima usata (se riguarda lo stesso progetto)
         if QSettings().value("/urmhs/lastUsedProjectName", "") == QgsProject.instance().baseName():
            self.urmhsLayerGroupList.setCurrentDbConn(QSettings().value("/urmhs/lastUsedConnectionInfo", ""))
      
      self.enableActions()
      
      conn = self.getCurrentDbConn(urmhsFunctionalityTypeEnum.STACK)
      if conn is None:
         return

      # leggo codice sessione corrente
      currentWrkSession = urmhs_stack.get_current_wrk_session_details(conn)
      if currentWrkSession is not None:
         if currentWrkSession.status == urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE:
            if urmhs_stack.wrk_session_set_active_status(conn, currentWrkSession.id, "Probable reactivation after a crash") == True:        
               msg = QApplication.translate("urmhs", "The current work session n.{0}, named {1}, created by {2} on {3}")
               msg = msg.format(str(currentWrkSession.id), currentWrkSession.name, currentWrkSession.created_by, str(currentWrkSession.creation_date))
               msg = msg + QApplication.translate("urmhs", " is active.")
               QMessageBox.information(None, "URMHS", msg)            
         elif currentWrkSession.status == urmhs_stack.urmhsWrkSessionStatusEnum.SUSPENDED:
            if urmhs_stack.wrk_session_set_active_status(conn, currentWrkSession.id) == True:
               msg = QApplication.translate("urmhs", "The current work session n.{0}, named {1}, created by {2} on {3}")
               msg = msg.format(str(currentWrkSession.id), currentWrkSession.name, currentWrkSession.created_by, str(currentWrkSession.creation_date))
               msg = msg + QApplication.translate("urmhs", " was suspended and now has been activated.")
               QMessageBox.information(None, "URMHS", msg)               
         elif currentWrkSession.status == urmhs_stack.urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE:
            msg = QApplication.translate("urmhs", "The current work sesssion n.{0}, named {1}, created by {2} on {3}")
            msg = msg.format(str(currentWrkSession.id), currentWrkSession.name, currentWrkSession.created_by, str(currentWrkSession.creation_date))
            msg = msg + QApplication.translate("urmhs", " is waiting for approval.")
            QMessageBox.information(None, "URMHS", msg)
      self.refreshWrkSessionLbl()
      
      
   def getCurrentDbConn(self, functionality = None):
      if self.urmhsLayerGroupList.currentUrmhsLayerGroup is not None:
         return self.urmhsLayerGroupList.currentUrmhsLayerGroup.getDbConn(functionality)
      else:
         return None
   

   def enableActions(self):
            
      conn = self.getCurrentDbConn(None)     
      if conn is None:
         # STACK
         # -----
         self.enableStack_action.setEnabled(False)
         self.disableStack_action.setEnabled(False)
         
         # HISTORY
         # -------
         self.enableHistory_action.setEnabled(False)
         self.disableHistory_action.setEnabled(False)
      else:
         currUser = urmhs_users.get_current_user_details(conn)
         superUser = True if currUser is not None and currUser.isSuperUser else False
         # STACK
         # -----
         self.enableStack_action.setEnabled(True if superUser else False)
         self.disableStack_action.setEnabled(True if superUser else False)
         # HISTORY
         # -------
         self.enableHistory_action.setEnabled(True if superUser else False)
         self.disableHistory_action.setEnabled(True if superUser else False)

         
      
      conn = self.getCurrentDbConn(urmhsFunctionalityTypeEnum.STACK)     
      if conn is None:
         # UNDO
         #-----
         self.undo_action.setEnabled(False)
         self.nUndo_action.setEnabled(False)
         self.undoBeginGroup_action.setEnabled(False)
         self.undoEndGroup_action.setEnabled(False)
         self.undoInsertBookmark_action.setEnabled(False)
         self.undoBookmark_action.setEnabled(False)
         self.setFirstEnabledDefaultAction(self.undoToolButton)
         # REDO
         #-----
         self.redo_action.setEnabled(False)
         self.nRedo_action.setEnabled(False)
         self.redoBookmark_action.setEnabled(False)
         self.setFirstEnabledDefaultAction(self.redoToolButton)
         # SESSIONI DI LAVORO
         # ------------------
         self.workSessionCreate_action.setEnabled(False)
         self.workSessionSave_action.setEnabled(False)
         self.workSessionDel_action.setEnabled(False)
         self.workSessionActivate_action.setEnabled(False)
         self.workSessionSuspend_action.setEnabled(False)
         self.workSessionList_action.setEnabled(False)
         self.workSessionChangeExecuter_action.setEnabled(False)
         self.setFirstEnabledDefaultAction(self.workSessionToolButton)
         
         # UTENTI
         # ------
         self.userManagement_action.setEnabled(False)
         self.userConfirm_action.setEnabled(False)
         self.setFirstEnabledDefaultAction(self.userToolButton)
      else:
         # verifico che esista un utente corrente
         currUser = urmhs_users.get_current_user_details(conn)
         # verifico che esista una sessione di lavoro corrente
         wrkSessionId = urmhs_stack.get_current_wrk_session_id(conn)
                  
         # UNDO
         is_undoable = urmhs_stack.undo_is_undoable(conn)
         self.undo_action.setEnabled(is_undoable)
         self.nUndo_action.setEnabled(is_undoable)
         self.undoBeginGroup_action.setEnabled(False if wrkSessionId is None else True)
         self.undoEndGroup_action.setEnabled(False if wrkSessionId is None else True)
         self.undoInsertBookmark_action.setEnabled(False if wrkSessionId is None else True)
         self.undoBookmark_action.setEnabled(is_undoable)
         self.setFirstEnabledDefaultAction(self.undoToolButton)
         # REDO
         is_redoable = urmhs_stack.undo_is_redoable(conn)
         self.redo_action.setEnabled(is_redoable)
         self.nRedo_action.setEnabled(is_redoable)
         self.redoBookmark_action.setEnabled(is_redoable)
         self.setFirstEnabledDefaultAction(self.redoToolButton)
         # SESSIONI DI LAVORO
         # ------------------
         self.workSessionCreate_action.setEnabled(False if currUser is None else True)
         self.workSessionSave_action.setEnabled(False if (currUser is None) or (wrkSessionId is None) else True)
         self.workSessionDel_action.setEnabled(False if currUser is None else True)
         self.workSessionActivate_action.setEnabled(False if currUser is None else True)
         self.workSessionSuspend_action.setEnabled(False if (currUser is None) or (wrkSessionId is None) else True)
         self.workSessionList_action.setEnabled(False if currUser is None else True)
         self.workSessionChangeExecuter_action.setEnabled(False if currUser is None else True)
         self.setFirstEnabledDefaultAction(self.workSessionToolButton)
         # UTENTI
         # ------
         self.userManagement_action.setEnabled(True)
         self.userConfirm_action.setEnabled(False if currUser is None else True)
         self.setFirstEnabledDefaultAction(self.userToolButton)
      
      self.setFirstEnabledDefaultAction(self.enableStackToolButton)         
      
      
      conn = self.getCurrentDbConn(urmhsFunctionalityTypeEnum.HISTORY)
      if conn is None:
         # HISTORY
         # -------
         self.setHistoryDate_action.setEnabled(False)
      else:
         currUser = urmhs_users.get_current_user_details(conn)
         
         # HISTORY
         # -------
         self.setHistoryDate_action.setEnabled(False if currUser is None else True)
         
      self.setFirstEnabledDefaultAction(self.enableHistoryToolButton)         
      
      self.setCurrentDBConnection_action.setEnabled(True)
      self.setFirstEnabledDefaultAction(self.utilityToolButton)
      
   # HELP
   # ----
   
   def doHelp(self):
      pass

   # UNDO \ REDO
   # -----------

   def doUndo(self):
      urmhs_stack.undo_op(self.getCurrentDbConn(), 1)
      self.urmhsLayerGroupList.repaintStackEnabledLayerList()
      self.enableActions()
      
      
   def doRedo(self):
      urmhs_stack.redo_op(self.getCurrentDbConn(), 1)
      self.urmhsLayerGroupList.repaintStackEnabledLayerList()
      self.enableActions()


   def doNUndo(self):
      title = QApplication.translate("urmhs", "URMHS - UNDO")
      msg = QApplication.translate("urmhs", "How many operations do you want to undo ? ")
      result, ok = QInputDialog.getInt(None, title, msg, 1, 1)
      if ok:
         urmhs_stack.undo_op(self.getCurrentDbConn(), result)
         self.urmhsLayerGroupList.repaintStackEnabledLayerList()
         self.enableActions()


   def doNRedo(self):
      title = QApplication.translate("urmhs", "URMHS - UNDO")
      msg = QApplication.translate("urmhs", "How many operations do you want to redo ? ")
      result, ok = QInputDialog.getInt(None, title, msg, 1, 1)
      if ok:
         urmhs_stack.redo_op(self.getCurrentDbConn(), result)
         self.urmhsLayerGroupList.repaintStackEnabledLayerList()
         self.enableActions()


   def doUndoBeginGroup(self):
      urmhs_stack.undo_insert_begin_group(self.getCurrentDbConn())
      self.enableActions()

   def doUndoEndGroup(self):
      urmhs_stack.undo_insert_end_group(self.getCurrentDbConn())
      self.enableActions()


   def doUndoInsertBookmark(self):
      urmhs_stack.undo_insert_bookmark(self.getCurrentDbConn())
      self.enableActions()

   def doUndoBookmark(self):
      urmhs_stack.undo_bookmark(self.getCurrentDbConn())
      self.urmhsLayerGroupList.repaintStackEnabledLayerList()
      self.enableActions()

   def doRedoBookmark(self):
      urmhs_stack.redo_bookmark(self.getCurrentDbConn())
      self.urmhsLayerGroupList.repaintStackEnabledLayerList()
      self.enableActions()


   # WORK SESSION
   # ------------
   
   def doWorkSessionCreate(self):
      dlg = urmhsCreateWrkSession_Dialog(None, self.getCurrentDbConn())
      if dlg.exec_() == QDialog.Accepted:
         self.enableActions()
         self.refreshWrkSessionLbl()



   def doCurrentWorkSessionSave(self):
      conn = self.getCurrentDbConn()
      currUser = urmhs_users.get_current_user_details(conn)
      if currUser is None:
         return
      
      wrkSession = urmhs_stack.get_current_wrk_session_details(conn)
      if wrkSession is None:
         msg = QApplication.translate("urmhs", "No current work session.")
         QMessageBox.critical(None, "URMHS", msg)
         return
         
      if currUser.isSuperUser or currUser.canSave:
         if urmhs_stack.current_wrk_session_save(conn) == True:
            msg = QApplication.translate("urmhs", "The current work session has been saved.")
            QMessageBox.information(None, "URMHS", msg)
            self.enableActions()
         else:
            msg = QApplication.translate("urmhs", "Current work session save failed.")
            QMessageBox.critical(None, "URMHS", msg)
      else:
         if urmhs_stack.wrk_session_set_wait_for_save_status(conn) == True:
            msg = QApplication.translate("urmhs", "The current work session has been set in \"waiting for approval\" status.")
            QMessageBox.information(None, "URMHS", msg)
            self.enableActions()
         else:
            msg = QApplication.translate("urmhs", "The current work session can't be set in \"waiting for approval\" status.")
            QMessageBox.critical(None, "URMHS", msg)
            
      self.refreshWrkSessionLbl()


   def doWorkSessionDel(self):
      dlg = urmhsWrkSessionList_Dialog(None, self.getCurrentDbConn(), urmhsWrkSessionListModeEnum.ERASE)
      if dlg.exec_() == QDialog.Accepted:
         self.urmhsLayerGroupList.repaintStackEnabledLayerList()
         self.enableActions()
         self.refreshWrkSessionLbl()


   def doWorkSessionActivate(self):
      dlg = urmhsWrkSessionList_Dialog(None, self.getCurrentDbConn(), urmhsWrkSessionListModeEnum.ACTIVATE)
      if dlg.exec_() == QDialog.Accepted:
         self.urmhsLayerGroupList.repaintStackEnabledLayerList()
         self.enableActions()
         self.refreshWrkSessionLbl()


   def doWorkSessionSetExecuter(self):
      dlg = urmhsWrkSessionList_Dialog(None, self.getCurrentDbConn(), urmhsWrkSessionListModeEnum.SET_EXECUTER)
      dlg.exec_()


   def doCurrentWorkSessionSuspend(self):
      conn = self.getCurrentDbConn()
      
      wrkSession = urmhs_stack.get_current_wrk_session_details(conn)
      if wrkSession is None:
         msg = QApplication.translate("urmhs", "No current work session.")
         QMessageBox.critical(None, "URMHS", msg)
         return
            
      msg = QApplication.translate("urmhs", "Are you sure you want to suspend the current work session (you can leave a note) ?")
      note, ok = QInputDialog.getText(None, "URMHS", msg)
      
      if ok:
         if urmhs_stack.wrk_session_set_suspended_status(conn, note) == False:
            msg = QApplication.translate("urmhs", "Current work session not suspended.")
            QMessageBox.critical(None, "URMHS", msg)
         self.enableActions()
         
      self.refreshWrkSessionLbl()

      
   def doWorkSessionList(self):
      dlg = urmhsWrkSessionList_Dialog(None, self.getCurrentDbConn(), urmhsWrkSessionListModeEnum.LIST_ALL)
      dlg.exec_()
      

   def doEnableStack(self):
      dlg = urmhsEnableStack_Dialog(None, self.getCurrentDbConn(), urmhsEnableStackModeEnum.ENABLE_STACK)
      if dlg.exec_() == QDialog.Accepted:
         self.enableActions()

      
   def doDisableStack(self):
      dlg = urmhsEnableStack_Dialog(None, self.getCurrentDbConn(), urmhsEnableStackModeEnum.DISABLE_STACK)
      if dlg.exec_() == QDialog.Accepted:
         self.enableActions()


   def doSetHistoryDate(self):
      if self.setHistoryDate_Dialog is not None:
         self.iface.removeDockWidget(self.setHistoryDate_Dialog)
         del self.setHistoryDate_Dialog
      self.setHistoryDate_Dialog = urmhsSetHistoryDate_Dialog(self)
      self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.setHistoryDate_Dialog)


   def doEnableHistory(self):
      dlg = urmhsEnableHistory_Dialog(None, self.getCurrentDbConn(), urmhsEnableHistoryModeEnum.ENABLE_HISTORY)
      if dlg.exec_() == QDialog.Accepted:
         self.enableActions()


   def doDisableHistory(self):
      dlg = urmhsEnableHistory_Dialog(None, self.getCurrentDbConn(), urmhsEnableHistoryModeEnum.DISABLE_HISTORY)
      if dlg.exec_() == QDialog.Accepted:
         self.enableActions()
   
   
   # UTENTI
   # ------


   def doUserConfirm(self):
      dlg = urmhsUserConfirm_Dialog(None, self.getCurrentDbConn())
      if dlg.exec_() == QDialog.Accepted:
         self.enableActions()

      
   def doUserManagement(self):
      dlg = urmhsUserList_Dialog(None, self.getCurrentDbConn())
      dlg.exec_()
         


      # UTILITA'
   # --------


   def doSetCurrentDBConnection(self):
      dlg = urmhsDBConnectionList_Dialog(None, self.urmhsLayerGroupList)
      if dlg.exec_() == QDialog.Accepted:
         conn = self.getCurrentDbConn()         
         if conn is not None:
            # leggo codice sessione corrente
            currentWrkSession = urmhs_stack.get_current_wrk_session_details(conn)
            if currentWrkSession is not None:
               if currentWrkSession.status == urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE:
                  if urmhs_stack.wrk_session_set_suspended_status(conn) == True:
                     msg = QApplication.translate("urmhs", "The current work session has been suspended.")
                     QMessageBox.information(None, "URMHS", msg)
                     
         layerGroup = dlg.getSelectLayerGroup()
         if layerGroup is not None:
            self.urmhsLayerGroupList.currentUrmhsLayerGroup = layerGroup
            QSettings().setValue("/urmhs/lastUsedProjectName", QgsProject.instance().baseName())
            QSettings().setValue("/urmhs/lastUsedConnectionInfo", layerGroup.connectionInfo())

         self.enableActions()



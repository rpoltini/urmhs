# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 User management

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
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
import psycopg2

from qgis.core import *
from qgis.gui import *
from qgis.utils import *

from . import urmhs_stack
from . import urmhs_history
from .urmhs_dbconnection import connectionChecker

#===============================================================================
# urmhsFunctionalityTypeEnum class.
#===============================================================================
class urmhsFunctionalityTypeEnum():
   STACK      = 0       # Work session
   HISTORY    = 1       # History


# Layer Group
class urmhsLayerGroupClass(QObject):
   

   def __init__(self, plugin):
      QObject.__init__(self)
      self.plugin = plugin
      self.connString = ''
      self.dbConn = None
      self.stackEnabledLayerList = []
      self.historyEnabledLayerList = []


   def __del__(self):
      if self.dbConn is not None:
         self.dbConn.close()
      del self.stackEnabledLayerList[:]
      del self.historyEnabledLayerList[:]


   #============================================================================
   # getDbConn
   #============================================================================
   def getDbConn(self, functionality = None):
      if functionality is None:
         return self.dbConn
      elif functionality == urmhsFunctionalityTypeEnum.STACK:
         # se non ci sono layer abilitati allo stack
         return None if len(self.stackEnabledLayerList) == 0 else self.dbConn
      elif functionality == urmhsFunctionalityTypeEnum.HISTORY:
         # se non ci sono layer abilitati alla storicizzazione
         return None if len(self.historyEnabledLayerList) == 0 else self.dbConn
      else:
         return None
      
   
   #============================================================================
   # connectionInfo senza info sensibili (password)
   #============================================================================
   def connectionInfo(self):
      if self.dbConn is not None:
         uri = QgsDataSourceUri(self.dbConn.dsn)
         return uri.connectionInfo()
      else:
         return ''


   def addLayer(self, layer):
      conn, connString = connectionChecker.check(layer)
      if conn is None:
         return False
      
      if self.connString != '':
         if self.connString != connString:
            return False      
         conn = self.dbConn
      
      uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri()) 
      isStackEnabled = urmhs_stack.is_stack_view(conn, uri.schema(), uri.table())
      isHistoryEnabled = urmhs_history.is_history_view(conn, uri.schema(), uri.table())
      if (not isStackEnabled) and (not isHistoryEnabled):
         return False 
      
      if self.connString == '':
         self.connString = connString
         self.dbConn = conn

      if isStackEnabled:
         self.stackEnabledLayerList.append(layer)
         
#          if layer.dataProvider().transaction(): # se il layer appartiene a un gruppo di transazione
#             layer.editCommandStarted.connect(self.onBeforeCommitChanges)
#          else:
         layer.editCommandStarted.connect(self.onEditCommandStarted)
         layer.editCommandEnded.connect(self.onEditCommandEnded)
         layer.editCommandDestroyed.connect(self.onEditCommandDestroyed)

      if isHistoryEnabled:
         self.historyEnabledLayerList.append(layer)

      return True


   def isLayerInStackEnabledLayerList(self, layer):
      try:
         self.stackEnabledLayerList.index(layer)
         return True
      except ValueError:
         return False


   def isLayerInHistoryLayerList(self, layer):
      try:
         self.historyEnabledLayerList.index(layer)
         return True
      except ValueError:
         return False

   
   def isLayerInGroup(self, layer):
      if self.isLayerInStackEnabledLayerList(layer):
         return True
      if self.isLayerInHistoryLayerList(layer):
         return True
      return False

   
   def delLayer(self, layer):
      result = False
      
      if self.isLayerInStackEnabledLayerList(layer):
         self.stackEnabledLayerList.remove(layer)
#          if layer.dataProvider().transaction():
#             layer.editCommandStarted.connect(self.onBeforeCommitChanges)
#          else:
         layer.editCommandStarted.disconnect(self.onEditCommandStarted)
         layer.editCommandEnded.disconnect(self.onEditCommandEnded)
         layer.editCommandDestroyed.connect(self.onEditCommandDestroyed)
         result = True
         
      if self.isLayerInHistoryLayerList(layer):
         self.historyEnabledLayerList.remove(layer)
         result = True

      return result
   
   
   def onEditCommandStarted(self, op_name):
      if self.dbConn is None:
         return
      layer = self.sender()
      uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())      
      quotedTablename = "\"" + uri.schema() + "\".\"" + urmhs_stack.get_table_name_from_stack_view_name(self.dbConn, uri.table()) + "\""      
      return urmhs_stack.op_begin(self.dbConn, op_name, ([quotedTablename],))


   def onEditCommandEnded(self):
      layer = self.sender()
      if layer.commitChanges() == False:
         layer.rollBack()
         if self.dbConn is not None:
            urmhs_stack.op_abandon_current(self.dbConn)
         
      layer.startEditing()
      self.plugin.enableActions()


   def onEditCommandDestroyed(self):
      if self.dbConn is None:
         return
      return urmhs_stack.op_abandon_current(self.dbConn)


   def onBeforeCommitChanges(self):
      if self.dbConn is None:
         return
      layer = self.sender()
      uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())      
      quotedTablename = "\"" + uri.schema() + "\".\"" + urmhs_stack.get_table_name_from_stack_view_name(self.dbConn, uri.table()) + "\""      
      return urmhs_stack.op_begin(self.dbConn, op_name, ([quotedTablename],))
   
   
   def repaintStackEnabledLayerList(self):
      for l in self.stackEnabledLayerList:
         l.triggerRepaint()
   
   
   # HISTORY
   # -------
   
   
   def repaintHistoryEnabledLayerList(self):
      for l in self.historyEnabledLayerList:
         l.triggerRepaint()


# Layer Group List
class urmhsLayerGroupListClass(QObject):


   def __init__(self, plugin):
      QObject.__init__(self)
      self.plugin = plugin
      self.urmhsLayerGroupList = []
      self.currentUrmhsLayerGroup = None


   #============================================================================
   # __del__
   #============================================================================
   def __del__(self):
      del self.urmhsLayerGroupList[:] # svuoto la lista


   #============================================================================
   # add_layer
   #============================================================================
   def add_layer(self, layer):
      conn, connString = connectionChecker.check(layer)
      if conn is None:
         return False
      
      found = False
      for lg in self.urmhsLayerGroupList:
         if lg.connString == connString:
            found = True
            if lg.addLayer(layer):
               if self.currentUrmhsLayerGroup is None: # se non è ancora stato settato il gruppo corrente
                  self.currentUrmhsLayerGroup = lg # setto il gruppo corrente
                  return True

      if found:
         return False
      
      # verifico se la connessione è a un db che supporta urmhs
      if is_urmhs_supported(conn) == False:
         return False

      lg = urmhsLayerGroupClass(self.plugin)
      lg.connString = connString
      lg.dbConn = conn
      self.urmhsLayerGroupList.append(lg)
      if self.currentUrmhsLayerGroup is None: # se non è ancora stato settato il gruppo corrente
         self.currentUrmhsLayerGroup = lg # setto il gruppo corrente
         
      return lg.addLayer(layer)


   #============================================================================
   # remove_layer
   #============================================================================
   def remove_layer(self, layer):
      if layer.type() != QgsMapLayer.VectorLayer:
         return False
      if layer.providerType() != "postgres":
         return False      
      uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
      connString = uri.connectionInfo()
      
      for lg in self.urmhsLayerGroupList:
         if lg.connString == connString:
            if lg.delLayer(layer) == True:
               if len(lg.stackEnabledLayerList) == 0:
                  if lg.dbConn is not None:
                     # leggo codice sessione corrente
                     currentWrkSession = urmhs_stack.get_current_wrk_session_details(lg.dbConn)
                     if currentWrkSession is not None:
                        if currentWrkSession.status == urmhs_stack.urmhsWrkSessionStatusEnum.ACTIVE:
                           if urmhs_stack.wrk_session_set_suspended_status(lg.dbConn) == True:
                              msg = QApplication.translate("urmhs", "The current work session has been suspended.")
                              QMessageBox.information(None, "URMHS", msg)                  
               return True
            else:
               return False

      return False


   #============================================================================
   # setCurrentDbConn
   #============================================================================
   def setCurrentDbConn(self, connectionInfo): # connectionInfo senza info sensibili (password)
      for lg in self.urmhsLayerGroupList:
         if lg.connectionInfo() == connectionInfo:
            self.currentUrmhsLayerGroup = lg
            return True
      return False


   #============================================================================
   # getList
   #============================================================================
   def getList(self):
      return self.urmhsLayerGroupList


   #============================================================================
   # init
   #============================================================================
   def init(self):
      self.currentUrmhsLayerGroup = None
      del self.urmhsLayerGroupList[:] # svuoto la lista
      for layer in QgsProject.instance().mapLayers().values():
         self.add_layer(layer)
         
         
   #============================================================================
   # repaintStackEnabledLayerList
   #============================================================================
   def repaintStackEnabledLayerList(self):
      # ridisegna solo i layer della connessione corrente
      if self.currentUrmhsLayerGroup is not None:
         self.currentUrmhsLayerGroup.repaintStackEnabledLayerList()
         
         
#============================================================================
# is_urmhs_supported
#============================================================================
def is_urmhs_supported(conn):
   # Verifica se la connessione è ad un database che supporta urmhs
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT * FROM urmhs.get_current_user_details()")
   except psycopg2.Error as e:
      cursor.close()
      return False # non è stato installato urnmhs
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False # non esiste l'utente corrente non è abilitato a urmhs 
   
   return True

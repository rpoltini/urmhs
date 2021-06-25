# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 enable/disable history dialog

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
from qgis.PyQt.QtWidgets import QInputDialog, QLineEdit
import psycopg2
from qgis.core import *


#######################################################################################
# Classe che verifica che le connessioni siano valide
class urmhsConnectionChecker():
   def __init__(self):
      self.originalConnInfoList = [] # lista delle connessioni originali
      self.validConnInfoList = [] # lista delle connessioni valide
   
   def __del__(self):
      del self.originalConnInfo
      del self.validConnInfoList
      
   def clear(self):
      del self.originalConnInfo[:]
      del self.validConnInfoList[:]
      

   def check(self, input):
      # riceve una connessione sotto forma di QgsDataSourceUri oppure QgsVectorLayer oppure QgsVectorDataProvider
      # prova a connettersi e se fallisce chiede login e password memorizzandosi la nuova connessione corretta
      # restituisce la connessione e la stringa di connessione valida
      if type(input) == QgsDataSourceUri:
         uri = input
      elif type(input) == QgsVectorLayer:
         if input.providerType() != "postgres":
            return None, None      
         uri = QgsDataSourceUri(input.dataProvider().dataSourceUri())
      elif type(input) == QgsVectorDataProvider:
         uri = QgsDataSourceUri(input.dataSourceUri())    
      else:
         return None, None

      originalConnInfo = uri.connectionInfo()
            
      if originalConnInfo in self.originalConnInfoList: # se esiste già uso quella valida
         connString = self.validConnInfoList[self.originalConnInfoList.index(originalConnInfo)]
      else:
         connString = originalConnInfo

      while True:
         try:
            conn = psycopg2.connect(connString)
            conn.autocommit = True
            if originalConnInfo not in self.originalConnInfoList:
               self.originalConnInfoList.append(originalConnInfo)
               self.validConnInfoList.append(connString)
               
            return conn, connString
         except psycopg2.Error:
            if uri.authConfigId() != "":               
               username, password = get_username_password_by_authcfg(uri.authConfigId())
               if username is not None: uri.setUsername(username)
               if password is not None: uri.setPassword(password)
            else:
               # QGIS caches the connection credentials inside QgsCredentials based on the connection info.
               (success, username, password ) = QgsCredentials.instance().get(originalConnInfo, None, None )
               # Put the credentials back (for yourself and the provider), as QGIS removes it when you "get" it
               if success:
                  QgsCredentials.instance().put(originalConnInfo, username, password )
               if username is not None: uri.setUsername(username)
               if password is not None: uri.setPassword(password)
               
            if uri.username() == "": # se manca il nome utente lo chiedo
               username, okPressed = QInputDialog.getText(None, 
                                                      "URMHS", 
                                                      "User name for <" +  uri.connectionInfo(False) + ">:",
                                                      QLineEdit.Normal,
                                                      "")
               if okPressed == False:
                  return None, None
               uri.setUsername(username)
            
            if uri.password() == "": # se manca la password la chiedo
               pwd, okPressed = QInputDialog.getText(None, 
                                                      "URMHS", 
                                                      "Password for <" +  uri.connectionInfo(False) + ">:",
                                                      QLineEdit.Password,
                                                      "")
               if okPressed == False:
                  return None, None
               uri.setPassword(pwd)
               
            connString = uri.connectionInfo()
            
   
def get_username_password_by_authcfg(authcf):
   # password encrypted in AuthManager
   auth_manager = QgsApplication.authManager()
   conf = QgsAuthMethodConfig()
   auth_manager.loadAuthenticationConfig(authcf, conf, True)
   if conf.id():
      username = conf.config('username', '')
      password = conf.config('password', '')
      return username, password


def get_postgres_conn_info_by_name(name):
   """ Read PostgreSQL connection details from QSettings stored by QGIS
   from https://github.com/lutraconsulting/qgis-discovery-plugin/blob/master/Discovery/dbutils.py
   """
   settings = QSettings()
   settings.beginGroup(u"/PostgreSQL/connections/" + selected)
   if not settings.contains("database"): # non-existent entry?
      return {}
   
   conn_info = dict()
   
   #Check if a service is provided
   service = settings.value("service", '', type=str)
   hasService = len(service) > 0
   if hasService:
      conn_info["service"] = service
   
   # password and username
   username = ''
   password = ''
   authconf = settings.value('authcfg', '')
   if authconf :
      # password encrypted in AuthManager
      auth_manager = QgsApplication.authManager()
      conf = QgsAuthMethodConfig()
      auth_manager.loadAuthenticationConfig(authconf, conf, True)
      if conf.id():
         username = conf.config('username', '')
         password = conf.config('password', '')
   else:
      # basic (plain-text) settings
      username = settings.value('username', '', type=str)
      password = settings.value('password', '', type=str)
   
   # password and username could be stored in environment variables
   # if not present in AuthManager or plain-text settings, do not
   # add it to conn_info at all
   if len(username) > 0:
      conn_info["user"] = username
   if len(password) > 0:
      conn_info["password"] = password
   
   host = settings.value("host", "", type=str)
   database = settings.value("database", "", type=str)
   port = settings.value("port", "", type=str)
   
   #Prevent setting host, port or database to empty string or default value
   #It may by set in a provided service and would overload it
   if len(host) > 0:
      conn_info["host"] = host
   if len(database) > 0:
      conn_info["database"] = database
   if len(port) > 0:
      conn_info["port"] = int(port)
   
   return conn_info

#===============================================================================
#  = variabile globale
#===============================================================================

connectionChecker = urmhsConnectionChecker()
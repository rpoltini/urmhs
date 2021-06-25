# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 help functions

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
from qgis.PyQt.QtGui import * # for QDesktopServices
import os.path

import urllib.parse
import platform



#===============================================================================
# showHelp
#===============================================================================
def showHelp(section = "", filename = "index", packageName = None):
   """
   show a help in the user's html browser.
   per conoscere la sezione/pagina del file html usare internet explorer,
   selezionare nella finestra di destra la voce di interesse e leggerne l'indirizzo dalla casella in alto.
   Questo perché internet explorer inserisce tutti i caratteri di spaziatura e tab che gli altri browser non fanno.
   """   
   try:
      source = ""
      if packageName is None:
         import inspect
         source = inspect.currentframe().f_back.f_code.co_filename
      else:
         source = sys.modules[packageName].__file__
   except:
      return

   # initialize locale
   userLocaleList = QSettings().value("locale/userLocale").split("_")
   language = userLocaleList[0]
   region = userLocaleList[1] if len(userLocaleList) > 1 else ""

   path = QDir.cleanPath(os.path.dirname(source) + "/help/help")
   helpPath = path + "_" + language + "_" + region # provo a caricare la lingua e la regione selezionate
   
   if not os.path.exists(helpPath):
      helpPath = path + "_" + language # provo a caricare la lingua
      if not os.path.exists(helpPath):
         helpPath = path + "_en" # provo a caricare la lingua inglese
         if not os.path.exists(helpPath):
            return
      
   helpfile = os.path.join(helpPath, filename + ".html")
   if os.path.exists(helpfile):
      url = "file:///"+helpfile

      if section != "":
         url = url + "#" + urllib.parse.quote(section)

      # la funzione QDesktopServices.openUrl in windows non apre la sezione
      if platform.system() == "Windows":
         import subprocess
         from _winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, OpenKey, QueryValue
         # In Py3, this module is called winreg without the underscore
         
         try: # provo a livello di utente
            with OpenKey(HKEY_CURRENT_USER, r"Software\Classes\http\shell\open\command") as key:
               cmd = QueryValue(key, None)
         except: # se non c'era a livello di utente provo a livello di macchina
            with OpenKey(HKEY_LOCAL_MACHINE, r"Software\Classes\http\shell\open\command") as key:
               cmd = QueryValue(key, None)
   
         if cmd.find("\"%1\"") >= 0:
            subprocess.Popen(cmd.replace("%1", url))
         else:    
            if cmd.find("%1") >= 0:
               subprocess.Popen(cmd.replace("%1", "\"" + url + "\""))       
            else:
               subprocess.Popen(cmd + " \"" + url + "\"")
      else:
         QDesktopServices.openUrl(QUrl(url))           

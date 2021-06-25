# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 set history date dialog

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
from qgis.PyQt.QtWidgets import QDockWidget
import datetime
from qgis.core import *

from . import urmhs_set_history_date_ui
from . import urmhs_layer_group
from . import urmhs_stack
from . import urmhs_history
from .urmhs_help import showHelp



#######################################################################################
# Classe che gestisce l'interfaccia grafica
class urmhsSetHistoryDate_Dialog(QDockWidget, QObject, urmhs_set_history_date_ui.Ui_set_history_date_dialog):
   def __init__(self, plugin):
      #QDockWidget.__init__(self, None, Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)           
      QDockWidget.__init__(self, plugin.iface.mainWindow())           
      self.plugin = plugin
      self.setupUi(self)
      self.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

      conn = self.plugin.getCurrentDbConn()
      if conn is not None:
         current_history_date = urmhs_history.get_current_history_date(conn)
         if current_history_date is None:
            self.dateTime.setDateTime(datetime.datetime.now())
         else:
            self.dateTime.setDateTime(current_history_date)


   def onSetHistoryDate(self):
      current_history_date = self.dateTime.dateTime()
      for urmhsLayerGroup in self.plugin.urmhsLayerGroupList.getList():
         urmhs_history.set_current_history_date(urmhsLayerGroup.dbConn, current_history_date)
         urmhsLayerGroup.repaintHistoryEnabledLayerList()



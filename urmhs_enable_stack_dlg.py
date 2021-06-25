# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 enable/disable stack dialog

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
from qgis.PyQt.QtWidgets import QApplication, QDialog, QMessageBox, QTreeWidgetItem
import psycopg2
from qgis.core import *
from qgis.PyQt.QtXml import QDomDocument

from . import urmhs_enable_stack_ui
from . import urmhs_stack
from . import urmhs_history
from .urmhs_help import showHelp
from .urmhs_dbconnection import connectionChecker
from numpy import source


#===============================================================================
# urmhsEnableStackModeEnum class.
#===============================================================================
class urmhsEnableStackModeEnum():
   ENABLE_STACK = 1 # per abilitare lo stack alle tabelle
   DISABLE_STACK = 2 # per disattivare lo stack alle tabelle


#######################################################################################
# Classe che gestisce l'interfaccia grafica
class urmhsEnableStack_Dialog(QDialog, QObject, urmhs_enable_stack_ui.Ui_enable_stack):
   def __init__(self, parent, conn, mode):
      QDialog.__init__(self, parent)      
      self.conn = conn
      self.mode = mode
      self.setupUi(self)
      
      if self.mode == urmhsEnableStackModeEnum.ENABLE_STACK:
         title = QCoreApplication.translate("urmhs", "URMHS - Enable db stack")
         labelTxt = QCoreApplication.translate("urmhs", "Layers that can be stack enabled:")
      else:
         title = QCoreApplication.translate("urmhs", "URMHS - Disable db stack")
         labelTxt = QCoreApplication.translate("urmhs", "Layers that can be stack disabled:")
         self.addToMap.setVisible(False)
         self.removeFromMap.setVisible(False)
         
      self.setWindowTitle(title)
      self.label.setText(labelTxt)

      self.initialization = True
      fillQTreeWidgetFromLegend(self.layerTree, self.mode)
      self.layerTree.expandAll()
      self.initialization = False


   def onItemChanged(self, item, i):
      if self.initialization == True:
         return

      self.initialization = True
      downRecursiveChecks(item)
      upRecursiveChecks(item)
      self.initialization = False


   def accept(self):
      res = True
      i = 0
      layerList = get_checked_layer_list(self.layerTree.topLevelItem(0))
      for layer in layerList:
         if self.mode == urmhsEnableStackModeEnum.ENABLE_STACK:
            if self.enableLayerStack(layer) == False:
               res = False
               break
         else:
            if self.disableLayerStack(layer) == False:
               res = False
               break
         i = i + 1
      
      if self.mode == urmhsEnableStackModeEnum.ENABLE_STACK:
         msg = QCoreApplication.translate("urmhs", "{0} layers has been stack enabled.")
      else:            
         msg = QCoreApplication.translate("urmhs", "{0} layers has been stack disabled.")         
      QMessageBox.information(None, "URMHS", msg.format(str(i)))
      
      if res == True:
         QDialog.accept(self)

   
   def reject(self):
      QDialog.reject(self)


   def onHelpButton(self):
      showHelp(QCoreApplication.translate("Help", "Enable stack"))


   def enableLayerStack(self, layer):
      uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
      
      if not urmhs_stack.is_stack_enabled(self.conn, uri.schema(), uri.table()):
         if urmhs_stack.enable_stack_usr_table(self.conn, uri.schema(), uri.table()) == False:
            msg = QCoreApplication.translate("urmhs", "{0}.{1} not stack enabled.")
            msg = msg.format(uri.schema(), uri.table())
            QMessageBox.critical(None, "URMHS", msg)
            return False

      if self.addToMap.checkState() == Qt.Checked:
         layerTreeLayer = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
         if layerTreeLayer.parent():
            parentNode = layerTreeLayer.parent()
         else:
            parentNode = QgsProject.instance().layerTreeRoot()   
            
         viewName = urmhs_stack.get_stack_view_name(self.conn, uri.table())
         uri.setDataSource(uri.schema(), viewName, uri.geometryColumn(), uri.sql(), uri.keyColumn())
         newLayer = layer.clone()
         if self.removeFromMap.checkState() != Qt.Checked:
            # devo cambiare il data source
            newLayer.setDataSource(uri.uri(), viewName, newLayer.providerType(), QgsDataProvider.ProviderOptions())
         else:
            # devo cambiare il data source
            newLayer.setDataSource(uri.uri(), layer.name(), newLayer.providerType(), QgsDataProvider.ProviderOptions())
   
         style = QDomDocument()
         errMsg = ""
         errMsg = layer.exportNamedStyle(style)
         if errMsg == "":
            newLayer.importNamedStyle(style)     

         res = QgsProject.instance().addMapLayers([newLayer], False) # addToLegend=False
         QgsLayerTreeUtils.insertLayerBelow(parentNode, layer, newLayer)

         if self.removeFromMap.checkState() == Qt.Checked:
            QgsProject.instance().removeMapLayer(layer.id())


   def disableLayerStack(self, layer):
      uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
      
      if urmhs_stack.is_stack_enabled(self.conn, uri.schema(), uri.table()):
         if urmhs_stack.disable_stack_usr_table(self.conn, uri.schema(), uri.table()) == False:
            msg = QCoreApplication.translate("urmhs", "{0}.{1} not stack disabled.")
            msg = msg.format(uri.schema(), uri.table())
            QMessageBox.critical(None, "URMHS", msg)
            return False

      layerTreeLayer = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
      if layerTreeLayer.parent():
         parentNode = layerTreeLayer.parent()
      else:
         parentNode = QgsProject.instance().layerTreeRoot()   
         
      viewName = urmhs_stack.get_stack_view_name(self.conn, uri.table())
      uri.setDataSource(uri.schema(), viewName, uri.geometryColumn(), uri.sql(), uri.keyColumn())
      # devo rimuovere i layer che fanno capo alla vista
      for l in QgsProject.instance().mapLayers().values():
         if l.type() == QgsMapLayer.VectorLayer:
            if l.dataProvider().dataSourceUri() == uri.uri():
               QgsProject.instance().removeMapLayer(l.id())
      

def downRecursiveChecks(item):
   checkState = item.checkState(0)
   for i in range(0, item.childCount()):
      item.child(i).setCheckState(0, checkState)
      downRecursiveChecks(item.child(i))


def upRecursiveChecks(item):
   parent = item.parent()
   if parent is None:
      return
   nChild = parent.childCount()
   if nChild == 0:
      return
   checkState = parent.child(0).checkState(0)
   for i in range(1, nChild):
      if checkState != parent.child(i).checkState(0):
         checkState = Qt.PartiallyChecked
         break
   parent.setCheckState(0, checkState)
   upRecursiveChecks(parent)


def fillQTreeWidgetFromLegend(treeWidget, mode):
   treeWidget.clear()
   root = QgsProject.instance().layerTreeRoot()
   item = QTreeWidgetItem(treeWidget)
   item.setText(0, QgsProject.instance().fileInfo().baseName())
   item.setIcon(0, QgsLayerTreeModel.iconGroup())
   item.setCheckState(0, Qt.Unchecked);
   treeWidget.addTopLevelItem(item)
   if addChildrenToQTreeWidget(root, item, mode) == 0:
      treeWidget.clear()

   
def addChildrenToQTreeWidget(parentSrcItem, parentDestItem, mode):
   i = 0
   for children in parentSrcItem.children():
      if children.nodeType() == QgsLayerTreeNode.NodeGroup:
         item = QTreeWidgetItem(parentDestItem)
         item.setCheckState(0, Qt.Unchecked);
         item.setText(0, str(children.name()))
         item.setIcon(0, QgsLayerTreeModel.iconGroup())
         parentDestItem.addChild(item)
         added = addChildrenToQTreeWidget(children, item, mode)
         if added == 0:
            parentDestItem.removeChild(item)
         else:
            i = i + added
      else: # QgsLayerTreeNode.NodeLayer:
         layer = children.layer()
         if isValidLayerForQTreeWidget(layer, mode):
            item = QTreeWidgetItem(parentDestItem)
            item.setCheckState(0, Qt.Unchecked);
            item.setText(0, layer.name())
            item.setIcon(0, getLayerIcon(layer))
            item.setData(0, Qt.UserRole, layer)
            parentDestItem.addChild(item)
            i = i + 1
   return i


def get_checked_layer_list(item):
   layerList = []
   
   if item.checkState(0):
      layer = item.data(0, Qt.UserRole)
      if layer is not None:
         layerList.append(layer)

   for i in range(item.childCount()):
      layerList.extend(get_checked_layer_list(item.child(i)))
         
   return layerList


def isValidLayerForQTreeWidget(layer, mode):
   conn, connString = connectionChecker.check(layer)
   if conn is None:
      return False
   uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
   
   # se si vuole abilitare lo stack
   if mode == urmhsEnableStackModeEnum.ENABLE_STACK:
      # scarto le viste su stack e su dati storici
      if urmhs_stack.is_stack_view(conn, uri.schema(), uri.table()):
         return False
      if urmhs_history.is_history_view(conn, uri.schema(), uri.table()):
         return False
      
      # scarto le tabelle che sono già abilitate allo stack
      if urmhs_stack.is_stack_enabled(conn, uri.schema(), uri.table()):
         return False
      # se ha il suffisso "_urmhs_history" si tratta di una tabella storica 
      if uri.table().endswith("_urmhs_history"):
         return False
      # se ha il suffisso "_urmhs_stack" si tratta di una tabella di stack 
      if uri.table().endswith("_urmhs_stack"):
         return False
      
      # tutti gli altri layer possono essere abilitati
      return True
   else: # se si vuole disabilitare lo stack
      # se è una tabella abilitata allo stack
      if urmhs_stack.is_stack_enabled(conn, uri.schema(), uri.table()) == True:
         return True
      
      # tutti gli altri layer non possono essere disabilitati
      return False

      
def getLayerIcon(layer):
   if layer.type() == QgsMapLayer.VectorLayer:
      geomType = layer.geometryType()
      if geomType == QgsWkbTypes.PointGeometry:
         return QgsLayerItem.iconPoint()
      elif geomType == QgsWkbTypes.LineGeometry:
         return QgsLayerItem.iconLine()
      elif geomType == QgsWkbTypes.PolygonGeometry:
         return QgsLayerItem.iconPolygon()
      elif geomType == QgsWkbTypes.NullGeometry:
         return QgsLayerItem.iconTable()
      else:
         return QgsLayerItem.iconDefault()
   elif layer.type() == QgsMapLayer.RasterLayer:
      return QgsLayerItem.iconRaster()
   else:
      return QgsLayerItem.iconDefault()
   
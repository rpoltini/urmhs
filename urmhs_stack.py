# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 Undo Redo Multiuser System using db stack

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
import qgis.utils
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsRectangle


#===============================================================================
# urmhsWrkSessionStatusEnum class.
#===============================================================================
class urmhsWrkSessionStatusEnum():
   SUSPENDED = 0 # sessione in sospensione
   ACTIVE = 1 # sessione attiva
   WAITING_FOR_SAVE = 2 # sessione in attesa di approvazione per essere salvata
   SAVED = 3 # sessione salvata


#===============================================================================
# urmhsOpTypeEnum class.
#===============================================================================
class urmhsOpTypeEnum():
   NONE = 0 # nessuno
   COMMAND = 1 # singolo comando
   BEGIN_GROUP = 2 # inizio di un gruppo di comandi
   END_GROUP = 3 # fine di un gruppo di comandi
   BOOKMARK = 4 # flag di segnalibro, significa che si tratta di un segno a cui si può ritornare


def wrkSessionStatusToString(status):
   if status == urmhsWrkSessionStatusEnum.ACTIVE:
      return QApplication.translate("urmhs", "Active")
   elif status == urmhsWrkSessionStatusEnum.SAVED:
      return QApplication.translate("urmhs", "Saved")
   elif status == urmhsWrkSessionStatusEnum.SUSPENDED:
      return QApplication.translate("urmhs", "Suspended")
   elif status == urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE:
      return QApplication.translate("urmhs", "Waiting for approval")
   else:
      return ''


def stringToWrkSessionStatus(string):
   if string == QApplication.translate("urmhs", "Active"):
      return urmhsWrkSessionStatusEnum.ACTIVE
   elif string == QApplication.translate("urmhs", "Saved"):
      return urmhsWrkSessionStatusEnum.SAVED
   elif string == QApplication.translate("urmhs", "Suspended"):
      return urmhsWrkSessionStatusEnum.SUSPENDED
   elif string == QApplication.translate("urmhs", "Waiting for approval"):
      return urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE
   else:
      return -1


# Work Session History Item
class urmhsWrkSessionHistoryItemClass(QObject):

   def __init__(self):
      QObject.__init__(self)
      self.author = ""
      self.date = None
      self.status = None
      self.executer = ""
      self.note = ""


# Work Session
class urmhsWrkSessionClass(QObject):

   def __init__(self, conn):
      QObject.__init__(self)
      self.conn = conn
      self.id = 0
      self.name = ""
      self.status = urmhsWrkSessionStatusEnum.SUSPENDED
      self.created_by = ""
      self.creation_date = None
      self.current_executer = ""
      self.current_note = ""
      self.saved_by = ""
      self.save_date = None
      self.descr = ""
      self.current_zoom = "" # x_min, y_min, x_max, y_max in una stringa (in LL 4326)
      self.current_image = None # QPixmap
      self.historyList = []


   def __del__(self):
      del self.historyList[:] # svuoto la lista


   def load_history_from_db(self):
      del self.historyList[:] # svuoto la lista
      
      # query the table     
      cursor = self.conn.cursor()
      try:
         cursor.execute("SELECT * from urmhs.get_wrk_session_history(%s)", (self.id,)) # SQL
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return

      colNames = [desc[0] for desc in cursor.description]
      for row in cursor:
         historyItem = urmhsWrkSessionHistoryItemClass()
         historyItem.author = row[colNames.index("author")]
         historyItem.date = row[colNames.index("date")]
         historyItem.status = row[colNames.index("status")]
         historyItem.executer = row[colNames.index("executer")]
         historyItem.note = row[colNames.index("note")]
         self.historyList.append(historyItem)
         
      cursor.close()
      
      
# Work Session List
class urmhsWrkSessionListClass(QObject):

   def __init__(self, conn):
      QObject.__init__(self)
      self.conn = conn
      self.wrkSessionList = []


   def __del__(self):
      del self.wrkSessionList[:] # svuoto la lista


   def load_from_db(self, sqlCond = '', synthetic = True):
      del self.wrkSessionList[:] # svuoto la lista
      
      # query the table     
      cursor = self.conn.cursor()
      try:
         cursor.execute("SELECT * from urmhs.get_wrk_session_list(%s) ORDER BY creation_date DESC", (sqlCond,)) # SQL
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return

      colNames = [desc[0] for desc in cursor.description]
      for row in cursor:
         wrkSession = urmhsWrkSessionClass(self.conn)
         wrkSession.id = row[colNames.index("id")]
         wrkSession.name = row[colNames.index("name")]
         wrkSession.status = row[colNames.index("status")]
         wrkSession.created_by = row[colNames.index("created_by")]
         wrkSession.creation_date = row[colNames.index("creation_date")]
         wrkSession.current_executer = row[colNames.index("current_executer")]
         wrkSession.current_note = row[colNames.index("current_note")]
         wrkSession.saved_by = row[colNames.index("saved_by")]
         wrkSession.save_date = row[colNames.index("save_date")]
         wrkSession.descr = row[colNames.index("descr")]
         if synthetic == True:
            wrkSession.current_zoom = ""
            wrkSession.current_image = None
         else:
            wrkSession.current_zoom = row[colNames.index("current_zoom")]
            wrkSession.current_image = binaryToQPixmap(row[colNames.index("current_image")])
         
         self.wrkSessionList.append(wrkSession)
         
      cursor.close()


   def load_from_db_suspended(self):
      self.load_from_db("status=" + urmhsWrkSessionStatusEnum.SUSPENDED)

   def load_from_db_active(self):
      self.load_from_db("status=" + urmhsWrkSessionStatusEnum.ACTIVE)

   def load_from_db_waiting_for_save(self):
      self.load_from_db("status=" + urmhsWrkSessionStatusEnum.WAITING_FOR_SAVE)

   def load_from_db_saved(self):
      self.load_from_db("status=" + urmhsWrkSessionStatusEnum.SAVED)


# FUNZIONI PER LO STACK DI UNDO/REDO
# ==================================


def enable_stack_usr_table(conn, schema, table):
   # Abilita una tabella utente al sistema di undo/redo e multiutenza
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.enable_stack_usr_table(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def disable_stack_usr_table(conn, schema, table):
   # Disabilita una tabella utente al sistema di undo/redo e multiutenza
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.disable_stack_usr_table(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def is_stack_enabled(conn, schema, table):
   # Ritorna true se la tabella è abilitata alla gestione dello stack
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.is_stack_enabled(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def is_stack_view(conn, schema, view):
   # Ritorna TRUE se la vista è usata per accedere alla tabella dello stack
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.is_stack_view(%s, %s)", (schema, view))
   except psycopg2.Error as e:
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def get_stack_view_name(conn, table_name):
   # Ritorna il nome della vista di stack da usare per tabella
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.get_stack_view_name(%s, FALSE)", (table_name,))
   except psycopg2.Error as e:
      cursor.close()
      return ''
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return ''
   
   return row[0]


def get_table_name_from_stack_view_name(conn, view_name):
   # Ritorna il nome della tabella a cui si riferisce la vista di stack
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.get_table_name_from_stack_view_name(%s)", (view_name,))
   except psycopg2.Error as e:
      cursor.close()
      return ''
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return ''
   
   return row[0]


# FUNZIONI PER LE SESSIONI DI LAVORO
# ==================================

def getCurrentZoom(destEPSG = 4326):
   # get current map canvas extent in LL (4326) in string format
   canvas = qgis.utils.iface.mapCanvas()
   srcCrs = canvas.mapSettings().destinationCrs()
   destCrs = QgsCoordinateReferenceSystem(destEPSG);
   tr = QgsCoordinateTransform(srcCrs, destCrs, QgsProject.instance())
   destExtent = tr.transform(canvas.extent())
   # Returns a string representation of form xmin,ymin : xmax,ymax : destEPSG
   return destExtent.toString() + ":" + str(destEPSG)
      

def setCurrentZoom(strRect):
    # set current map canvas extent from a string in LL (4326)
   if strRect is None or len(strRect) == 0: return;
   
   canvas = qgis.utils.iface.mapCanvas()
   vertices = strRect.split(":")
   minCoords = vertices[0].split(",")
   maxCoords = vertices[1].split(",")
   srid = int(vertices[2])
   src = QgsCoordinateReferenceSystem(srid)
   dst = canvas.mapSettings().destinationCrs()
   tr = QgsCoordinateTransform(src, dst, QgsProject.instance())
   rect = QgsRectangle(float(minCoords[0]), float(minCoords[1]), float(maxCoords[0]), float(maxCoords[1]))
   canvas.zoomToFeatureExtent(tr.transform(rect))

   
def getCurrentMapCanvasImage():
   canvas = qgis.utils.iface.mapCanvas()
   return canvas.grab() # QPixmap
   

def QPixmapToBinary(inPixmap): # image = QPixmap
   byteArray = QByteArray()
   buffer = QBuffer(byteArray)
   buffer.open(QIODevice.WriteOnly)
   inPixmap.save(buffer, "PNG") # writes image into ba in PNG format   
   return psycopg2.Binary(byteArray) # byteArray to binary
   
   
def binaryToQPixmap(inBinary):
   pixmap = QPixmap()
   pixmap.loadFromData(inBinary)
   return pixmap
   

def get_current_wrk_session_details(conn):
   # verifico che esista una sessione di lavoro corrente
   if get_current_wrk_session_id(conn) is None:
      return None
   
   # Restituisce i dettagli della sessione di lavoro corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT * FROM urmhs.get_current_wrk_session_details()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return None
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return None
   
   colNames = [desc[0] for desc in cursor.description]
   wrkSession = urmhsWrkSessionClass(conn)
   wrkSession.id = row[colNames.index("id")]
   wrkSession.name = row[colNames.index("name")]
   wrkSession.status = row[colNames.index("status")]
   wrkSession.created_by = row[colNames.index("created_by")]
   wrkSession.creation_date = row[colNames.index("creation_date")]
   wrkSession.current_executer = row[colNames.index("current_executer")]
   wrkSession.current_note = row[colNames.index("current_note")]
   wrkSession.saved_by = row[colNames.index("saved_by")]
   wrkSession.save_date = row[colNames.index("save_date")]
   wrkSession.descr = row[colNames.index("descr")]
   wrkSession.current_zoom = row[colNames.index("current_zoom")]
   wrkSession.current_image = binaryToQPixmap(row[colNames.index("current_image")])

   return wrkSession


def get_current_wrk_session_id(conn):
   # Restituisce il codice della sessione di lavoro corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.get_current_wrk_session_id()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return None
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return None
   
   return row[0]


def set_current_wrk_session_id(conn, current_wrk_session_id):
   # Setta il codice di sessione corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.set_current_wrk_session_id(%s)", (current_wrk_session_id,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def get_next_wrk_session_id(conn):
   # Restituisce il prossimo codice di una sessione di lavoro
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.get_next_wrk_session_id()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return -1
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return -1
   
   return row[0]


def wrk_session_create(conn, wrk_session_name, wrk_session_descr, wrk_session_executor, wrk_session_note, wrk_session_id = -1):
   # Crea una sessione di lavoro
   strZoom = getCurrentZoom()
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_create(%s, %s, %s, %s, %s, %s)", \
                     (wrk_session_name, wrk_session_descr, wrk_session_executor, wrk_session_note, strZoom, wrk_session_id))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return -1
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return -1
   
   return row[0]


def wrk_session_delete(conn, wrk_session_id):
   # Cancella una sessione di lavoro senza salvare le modifiche
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_delete(%s)", (wrk_session_id,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def wrk_session_set_wait_for_save_status(conn, note = None):
   # Imposta lo stato di sessione "in attesa di approvazione per essere salvata"
   strZoom = getCurrentZoom()
   image = QPixmapToBinary(getCurrentMapCanvasImage())
   
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_set_wait_for_save_status(%s, %s, %s)", (strZoom, image, note))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def wrk_session_set_active_status(conn, wrk_session_id, note = None):
   # Imposta lo stato di sessione "sessione attiva"
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_set_active_status(%s, %s)", (wrk_session_id, note))
         
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   currentWrksSession = get_current_wrk_session_details(conn)
   setCurrentZoom(currentWrksSession.current_zoom)
   
   return row[0]


def wrk_session_set_suspended_status(conn, note = None):
   # Imposta lo stato di sessione "sessione sospesa"
   strZoom = getCurrentZoom()
   image = QPixmapToBinary(getCurrentMapCanvasImage())   

   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_set_suspended_status(%s, %s, %s)", (strZoom, image, note))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def current_wrk_session_save(conn, note = None):
   # Salva le modifiche della sessione di lavoro corrente
   strZoom = getCurrentZoom()
   image = QPixmapToBinary(getCurrentMapCanvasImage())
   
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_save(%s, %s, %s)", (strZoom, image, note))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def wrk_session_set_executer(conn, wrk_session_id, new_executer, note = None):
   # Imposta lo stato di sessione "sessione attiva"
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.wrk_session_set_executer(%s, %s, %s)", (wrk_session_id, new_executer, note))
         
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


# FUNZIONI PER LE OPERAZIONI NELLE SESSIONI DI LAVORO - OPERAZIONI
# ================================================================


def op_begin(conn, op_name, table_name_list):
   # Inizia una operazione nella sessione di lavoro corrente che coinvolge una lista di tabelle utente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.op_begin(%s, %s)", (op_name, table_name_list))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def op_add_table_to_current(conn, table_name):
   # Nella sessione di lavoro aggiunge una tabella utente alla lista delle tabelle utente coinvolte dall'operazione corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.op_add_table_to_current(%s)", (table_name,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def op_abandon_current(conn):
   # Abbandona l'operazione corrente nella sessione di lavoro corrente senza confermare le modifiche
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.op_abandon_current()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


# FUNZIONI PER LE OPERAZIONI NELLE SESSIONI DI LAVORO - UNDO/REDO
# ===============================================================


def undo_is_undoable(conn):
   # Restituisce TRUE se la sessione corrente è nelle condizioni di eseguire la funzione di UNDO altrimenti restituisce FALSE
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_is_undoable()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def undo_is_redoable(conn):
   # Restituisce TRUE se la sessione corrente è nelle condizioni di eseguire la funzione di REDO altrimenti restituisce FALSE
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_is_redoable()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def undo_op(conn, n_times):
   # Nella sessione di lavoro corrente esegue la funzione di UNDO n volte
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_op(%s)", (n_times,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def redo_op(conn, n_times):
   # Nella sessione di lavoro corrente esegue la funzione di REDO n volte
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.redo_op(%s)", (n_times,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


# GROUP
# =====


def undo_insert_begin_group(conn):
   # Inserisce un marcatore di inizio gruppo di operazioni nella sessione di lavoro corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_insert_begin_group()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def undo_insert_end_group(conn):
   # Inserisce un marcatore di fine gruppo di operazioni nella sessione di lavoro corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_insert_end_group()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


# BOOKMARK
# ========


def undo_insert_bookmark(conn):
   # Inserisce un bookmark nella sessione di lavoro corrente
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_insert_bookmark()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def undo_bookmark(conn):
   # Nella sessione di lavoro corrente esegue la funzione di UNDO fino ad incontrare il primo bookmark
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.undo_bookmark()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def redo_bookmark(conn):
   # Nella sessione di lavoro esegue la funzione di REDO fino ad incontrare il primo bookmark
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.redo_bookmark()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]



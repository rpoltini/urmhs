# -*- coding: utf-8 -*-
"""
/***************************************************************************
 urmhs Undo Redo Multiuser History System

 History system
 
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
from qgis.PyQt.QtWidgets import QMessageBox
import psycopg2


def enable_history_usr_table(conn, schema, table):
   # Abilita una tabella utente alla storicizzazione dei dati
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.enable_history_usr_table(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def disable_history_usr_table(conn, schema, table):
   # Disabilita una tabella utente alla storicizzazione dei dati
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.disable_history_usr_table(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def is_history_enabled(conn, schema, table):
   # Ritorna true se la tabella è abilitata alla storicizzazione
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.is_history_enabled(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def is_history_view(conn, schema, table):
   # Ritorna TRUE se la vista è usata per accedere alla tabella storica
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.is_history_view(%s, %s)", (schema, table))
   except psycopg2.Error as e:
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def get_current_history_date(conn):
   # Ritorna il momento storico in cui visualizzare i dati storici
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT current_history_date FROM urmhs.get_current_user_details()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return None
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return None
   
   return row[0]


def set_current_history_date(conn, current_history_date):
   # Setta il momento storico in cui visualizzare i dati storici      
   cursor = conn.cursor()
   try:
      if type(current_history_date) == QDateTime:
         cursor.execute("SELECT urmhs.set_current_history_date(%s::timestamp without time zone)", (current_history_date.toString(Qt.ISODate),))
      else:
         cursor.execute("SELECT urmhs.set_current_history_date(%s::timestamp without time zone)", (current_history_date,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def get_history_view_name(conn, table_name):
   # Ritorna il nome della vista dello storico da usare per tabella
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.get_history_view_name(%s, FALSE)", (table_name,))
   except psycopg2.Error as e:
      cursor.close()
      return ''
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return ''
   
   return row[0]

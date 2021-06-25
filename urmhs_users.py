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
from qgis.PyQt.QtWidgets import QMessageBox

import psycopg2
from psycopg2 import sql


# User
class urmhsUserClass(QObject):

   def __init__(self):      
      self.login = ''
      self.isSuperUser = False
      self.canSave = False
      self.security_question = ''
      

# User List
class urmhsUserListClass(QObject):

   def __init__(self, conn):
      # uri di tipo QgsDataSourceUri
      self.conn = conn
      self.userList = []
      self.load_from_db()


   def __del__(self):
      del self.userList[:] # svuoto la lista


   def load_from_db(self, sqlCond = ''):
      del self.userList[:] # svuoto la lista
      if self.conn is None:
         QMessageBox.critical(self, "", "Connessione al server postgres non valida.")
         return
      
      # query the table     
      cursor = self.conn.cursor()
      stm = "SELECT login,superuser,save,security_question FROM urmhs.login_roles"
      if len(sqlCond) > 0:
         stm = stm + " WHERE " + sqlCond
      stm = stm + " ORDER BY login"
      try:
         cursor.execute(stm) # SQL
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return

      for row in cursor:
         user = urmhsUserClass()
         user.login = row[0]
         user.isSuperUser = row[1]
         user.canSave = row[2]
         user.security_question = row[3]
         self.userList.append(user)
      cursor.close()


   def add_user_to_db(self, user, security_answer):
      if self.conn is None:
         QMessageBox.critical(self, "", "Connessione al server postgres non valida.")
         return False
      cursor = self.conn.cursor()
      stm1 = "INSERT INTO urmhs.login_roles (login, superuser, save, security_question, security_answer) VALUES "
      stm1 = stm1 + "(%s, %s, %s, %s, md5(%s))"
      values1 = (user.login, user.isSuperUser, user.canSave, user.security_question, security_answer)
      
      stm2 = psycopg2.sql.SQL("GRANT USAGE ON SCHEMA urmhs TO {};").format(sql.Identifier(user.login))
      stm3 = psycopg2.sql.SQL("GRANT USAGE ON ALL SEQUENCES IN SCHEMA urmhs TO {};").format(sql.Identifier(user.login))
                              
      try:
         cursor.execute(stm1, values1)
         cursor.execute(stm2)
         cursor.execute(stm3)
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return False

      cursor.close()
      self.userList.append(user)
      return True
      

   def del_user_to_db(self, user_login):
      if self.conn is None:
         QMessageBox.critical(self, "", "Connessione al server postgres non valida.")
         return False
      cursor = self.conn.cursor()
      stm1 = "DELETE FROM urmhs.login_roles WHERE login=%s"
      stm2 = psycopg2.sql.SQL("REVOKE USAGE ON SCHEMA urmhs FROM {};").format(sql.Identifier(user_login))
      stm3 = psycopg2.sql.SQL("REVOKE USAGE ON ALL SEQUENCES IN SCHEMA urmhs FROM {};").format(sql.Identifier(user_login))
      
      try:
         cursor.execute(stm1, (user_login,))
         cursor.execute(stm2)
         cursor.execute(stm3)
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return False
         
      cursor.close()
      for i in range(0, len(self.userList)):
         if self.userList[i].login == user_login:
            del self.userList[i]
            return True
         
      return True


   def upd_user_to_db(self, old_user_login, user):
      if self.conn is None:
         QMessageBox.critical(self, "", "Connessione al server postgres non valida.")
         return False
      cursor = self.conn.cursor()
      stm = "UPDATE urmhs.login_roles SET login=%s, superuser=%s, save=%s, security_question=%s WHERE login=%s"
      values = (user.login, user.isSuperUser, user.canSave, user.security_question, old_user_login)
      try:
         cursor.execute(stm, values)
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return False
         
      cursor.close()
      
      for i in range(0, len(self.userList)):
         if self.userList[i].login == old_user_login:
            self.userList[i].login = user.login
            self.userList[i].isSuperUser = user.isSuperUser
            self.userList[i].canSave = user.canSave
            self.userList[i].security_question = user.security_question
            return True
         
      return True


   def upd_user_security_to_db(self, user_login, security_question, security_answer):
      if self.conn is None:
         QMessageBox.critical(self, "", "Connessione al server postgres non valida.")
         return False
      cursor = self.conn.cursor()
      stm = "UPDATE urmhs.login_roles SET security_question=%s, security_answer=md5(%s) WHERE login=%s"
      values = (security_question, security_answer, user_login)
      try:
         cursor.execute(stm, values)
      except psycopg2.Error as e:
         QMessageBox.critical(None, "URMHS", e.pgerror)
         cursor.close()
         return False
         
      cursor.close()

      for i in range(0, len(self.userList)):
         if self.userList[i].login == user_login:
            self.userList[i].security_question = security_question
            return True
         
      return True


# UTENTI
# ======


def is_current_superuser(conn):
   # Restituisce TRUE se l'utente corrente è un superuser di urmhs
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.is_current_superuser()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return None
   
   row = cursor.fetchone()
   cursor.close()
 
   if row is None:
      return False
   
   return row[0]


def get_current_user_details(conn):
   # Restituisce un oggetto urmhsUserClass dell'utente corrente.
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT * FROM urmhs.get_current_user_details()")
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return None
   
   row = cursor.fetchone()
   colNames = [desc[0] for desc in cursor.description]
   cursor.close()
   if row is None:
      return None

   user = urmhsUserClass()
   user.login = row[colNames.index("login")]
   user.isSuperUser = row[colNames.index("superuser")]
   user.canSave = row[colNames.index("save")]
   user.securityQuestion = row[colNames.index("security_question")]
   user.securityAnswer = row[colNames.index("security_answer")]
   
   return user


def force_current_inet_client_addr(conn, security_answer):
   # Forza l'indirizzo di rete del client corrente per l'utente corrente.
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT urmhs.force_current_inet_client_addr(%s)", (security_answer,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


def quote_literal(conn, str):
   # Return the given string suitably quoted to be used as a string literal in an SQL statement string
   cursor = conn.cursor()
   try:
      cursor.execute("select quote_literal(%s)", (str,))
   except psycopg2.Error as e:
      QMessageBox.critical(None, "URMHS", e.pgerror)
      cursor.close()
      return False
   
   row = cursor.fetchone()
   cursor.close()
   if row is None:
      return False
   
   return row[0]


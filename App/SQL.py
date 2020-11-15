import sqlite3
import os

class SQL:
	conn = None
	c = None

	def __init__(self):
		self.conn = sqlite3.connect('sim.db')
		self.c = self.conn.cursor()

		print("DB CONNECTED")

		if os.stat("sim.db").st_size == 0:
			print("Configure data base...")
			self.c.execute('CREATE TABLE sms (row_id INTEGER PRIMARY KEY, number, msg, date)')
			self.c.execute('CREATE TABLE mms (row_id INTEGER PRIMARY KEY, number, date, unique_id, file BLOB, file_type, file_name)')
			self.conn.commit()



	def execute(self, sql, ar=None):
		self.c.execute(sql, ar)
		self.conn.commit()


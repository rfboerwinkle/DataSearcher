import sqlite3
from os.path import exists
import json

TRUE = "t"
FALSE = "f"
NA = "na"

class DB:
	def normalize(datum):
		return datum.strip(" \n\t\r").lower()

	def __init__(self, name):
		toCreate = not exists(name):

		self.connection = sqlite3.connect(name)
		self.cursor = self.connection.cursor()

		if toCreate:
			print("Database doesn't exist, initializing one...")
			# I didn't use ROWID becuase "VACUUM" reorganizes it
			self.cursor.execute("""CREATE TABLE tags (
				id INTIGER PRIMARY KEY
				groupName TEXT NOT NULL,
				value TEXT
			)""")
			self.cursor.execute("INSERT INTO tags (groupName, value) VALUES (?,?,?)", (0, "exists", TRUE))

			self.cursor.execute("""CREATE TABLE data (
				name TEXT NOT NULL,
				tagID INTEGER NOT NULL
			)""")

	def addTagGroup(name, values=(None,)):
		pass
	def addTagValue(groupName, value):
		pass
	def addDatum(name, tagIDs=(0,)):
		pass

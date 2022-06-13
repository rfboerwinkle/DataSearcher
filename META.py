import sqlite3
from os.path import exists
import json

TRUE = "t"
FALSE = "f"
NA = "na"

def normalize(datum):
	return datum.strip(" \n\t\r").lower()

class DB:
	def __init__(self, name):
		toCreate = not exists(name)

		self.connection = sqlite3.connect(name)
		self.cursor = self.connection.cursor()

		if toCreate:
			print("Database doesn't exist, initializing one...")
			# I didn't use ROWID becuase "VACUUM" reorganizes it
			self.cursor.execute("""CREATE TABLE tagGroups (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL UNIQUE
			) WITHOUT ROWID""")
			self.curTagGroupID = -1

			self.cursor.execute("""CREATE TABLE tags (
				id INTEGER PRIMARY KEY,
				tagGroupID INTEGER NOT NULL,
				name TEXT NOT NULL,
				FOREIGN KEY(tagGroupID) REFERENCES tagGroups(id)
			) WITHOUT ROWID""")
			self.curTagID = -1

			self.cursor.execute("""CREATE TABLE data (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL UNIQUE
			) WITHOUT ROWID""")
			self.curDatumID = -1

			self.cursor.execute("""CREATE TABLE tagging (
				datumID INTEGER NOT NULL,
				tagID INTEGER NOT NULL,
				FOREIGN KEY(datumID) REFERENCES data(id),
				FOREIGN KEY(tagID) REFERENCES tags(id)
			)""")

			self.connection.commit()

		else:
			self.cursor.execute("SELECT MAX(id) FROM tagGroups")
			self.curTagGroupID = self.cursor.fetchall()[0][0]
			if self.curTagGroupID == None:
				self.curTagGroupID = -1
			print("Highest tagGroupID:", self.curTagGroupID)

			self.cursor.execute("SELECT MAX(id) FROM tags")
			self.curTagID = self.cursor.fetchall()[0][0]
			if self.curTagID == None:
				self.curTagID = -1
			print("Highest tagID:", self.curTagID)

			self.cursor.execute("SELECT MAX(id) FROM data")
			self.curDatumID = self.cursor.fetchall()[0][0]
			if self.curDatumID == None:
				self.curDatumID = -1
			print("Highest DatumID:", self.curDatumID)

	def commit(self):
		self.connection.commit()

	def addTagGroup(self, name):
		self.curTagGroupID += 1
		self.cursor.execute("INSERT INTO tagGroups (id,name) VALUES (?,?)", (self.curTagGroupID, name))
		return self.curTagGroupID

	def addTag(self, tagGroupName, name): # TODO fix
		self.curTagID += 1
		self.cursor.execute("""INSERT INTO tags (id,tagGroupID,name) VALUES (?,
			(SELECT id FROM tagGroups WHERE name = ? LIMIT 1)
		,?)""", (self.curTagID, tagGroupName, name))
		return self.curTagID

	def addDatum(self, name):
		self.curDatumID += 1
		self.cursor.execute("INSERT INTO data (id,name) VALUES (?,?)", (self.curDatumID, name))
		return self.curDatumID

	def tagDatum(self, datumName, tagGroupName, tagName): # TODO fix
		self.cursor.execute("""INSERT INTO tagging (datumID,tagID) VALUES (
			(SELECT id FROM data WHERE name = ? LIMIT 1),
			(SELECT id FROM tags WHERE name = ? AND tagGroupID =
				(SELECT id FROM tagGroups WHERE name = ? LIMIT 1)
			LIMIT 1)
		)""", (datumName, tagName, tagGroupName))

	def untagDatum(self, datumName, tagName):
		pass

	def getTagGroups(self):
		self.cursor.execute("SELECT name FROM tagGroups ORDER BY name")
		return self.cursor.fetchall()

	def getTags(self, tagGroupName):
		self.cursor.execute("""SELECT name FROM tags WHERE tagGroupID =
			(SELECT id FROM tagGroups WHERE name = ? LIMIT 1)
		ORDER BY name""", (tagGroupName,))
		return self.cursor.fetchall()

	def getData(self):
		self.cursor.execute("SELECT name FROM data ORDER BY name")
		return self.cursor.fetchall()

	def getDatum(self, name):
		self.cursor.execute("""SELECT tagGroups.name,tags.name FROM tags
		JOIN tagGroups ON tags.tagGroupID = tagGroups.id
		WHERE tags.id IN
			(SELECT tagID FROM tagging WHERE datumID =
				(SELECT id FROM data WHERE name = ? LIMIT 1)
			)
		ORDER BY tagGroups.name,tags.name""", (name,))
		return self.cursor.fetchall()

	def editTag(self, groupName, oldName, newName): # all data with this tag will change
		pass
	def editTagGroup(self, oldGroupName, newGroupName):
		pass

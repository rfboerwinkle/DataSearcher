import sqlite3

def newDatabase(name):
	db = sqlite3.connect(name)
	cursor = db.cursor()

from wordMethods.haiku import createEvolvedHaiku

print createEvolvedHaiku()

'''
from dataCreation.populateData import DatabaseInit

d = DatabaseInit()

d.TablesInit()
'''

'''
import sqlite3

conn = sqlite3.connect("data/haiku.db")
c = conn.cursor()

for row in c.execute("select firstPos,firstWord from Bigrams"):
	print row[0]
	print row[1]	

'''

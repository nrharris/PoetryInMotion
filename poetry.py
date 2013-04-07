#from wordMethods.haiku import createEvolvedHaiku

#print createEvolvedHaiku()

'''
from dataCreation.populateData import DatabaseInit

d = DatabaseInit()

d.TablesInit()
'''

#'''
import sqlite3

conn = sqlite3.connect("data/haiku.db")
c = conn.cursor()

for row in c.execute("select firstPos,firstWord,firstSyllables,secondPos,secondWord,secondSyllables from Bigrams"):
	
	print str(row[0]) + " " + str(row[1]) + " " + str(row[2])
	print str(row[3]) + " " + str(row[4]) + " " + str(row[5])
#'''

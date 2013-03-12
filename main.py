import sqlite3

x = sqlite3.connect("data/haiku.db")

cursor = x.cursor()

cursor.execute("select * from PosBigrams")
print cursor.fetchall()

#from wordMethods.haiku import createNaiveHaiku

#createNaiveHaiku()

#from dataCreation.populateData import DatabaseInit

#x = DatabaseInit()
#x.initialize()


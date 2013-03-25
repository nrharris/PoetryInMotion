import sqlite3
import itertools

def pos(haiku):
	
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
	
	connection = sqlite3.connect("data/haiku.db")
	cursor = connection.cursor()
	
	posList = []
 	
	for i in xrange(len(words)-1):
		firstWord = words[i]
		secondWord = words[i+1]
		cursor.execute("select firstPos from Bigrams where firstWord = ? and secondWord = ?",(firstWord,secondWord))
		
		try:
			posList.append((firstWord,cursor.fetchone()[0]))
		except:
			print firstWord + " " + secondWord + " Failed"
	return posList

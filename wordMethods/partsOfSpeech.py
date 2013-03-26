import sqlite3
import itertools

def pos(haiku):
	
	splits = [line.split(" ") for line in haiku.split("\n")]	
	#words = [str(word) for word in list(itertools.chain(*splits))]
	
	connection = sqlite3.connect("data/haiku.db")
	cursor = connection.cursor()
	
 	posList = []	
	
	lineCount = 0
	for line in splits:
		lineCount+=1
		for i in xrange(0,len(line)-1,2):
			firstWord = line[i]
			secondWord = line[i+1]
			cursor.execute("select firstPos,secondPos from Bigrams where firstWord = ? and secondWord = ?",(firstWord,secondWord))
	
			try:
				posList.append((firstWord,cursor.fetchone()[0],lineCount))
				posList.append((secondWord,cursor.fetchone()[1],lineCount))
			except:
				pass
	return posList

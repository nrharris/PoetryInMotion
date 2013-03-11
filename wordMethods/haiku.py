from sounds import SyllableCounter
from random import randint
import sqlite3

def isHaiku(text):
	sc = SyllableCounter()
	counts = sc.getLineCounts(text)
	expectedCounts = [5,7,5]
	
	if not counts:
		return False

	if len(counts) != 3:
		return false

	for i in xrange(len(expectedCounts)):
		if counts[i] != expectedCounts[i]:
			return False

	return True	

def createNaiveHaiku():
	connection = sqlite3.connect('data/haiku.db')
	cursor = connection.cursor()
	cursor.execute("select count(*) from FiveSyllables")
	numFiveRecords = cursor.fetchone()[0]
	cursor.execute("select count(*) from SevenSyllables")
	numSevenRecords = cursor.fetchone()[0]

	firstIndex = int(randint(1,numFiveRecords))
	secondIndex = int(randint(1,numSevenRecords))
	thirdIndex = int(randint(1,numFiveRecords))
	
	cursor.execute("select segment from FiveSyllables where id = ?",(firstIndex,))
	print cursor.fetchone()[0]
	cursor.execute("select segment from SevenSyllables where id = ?",(secondIndex,))
	print cursor.fetchone()[0]
	cursor.execute("select segment from FiveSyllables where id = ?",(thirdIndex,))
	print cursor.fetchone()[0]
		

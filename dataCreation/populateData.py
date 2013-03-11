import sqlite3
from wordMethods.sounds import SyllableCounter

class DatabaseInit:

	def __init__(self):
		self.connection = sqlite3.connect('data/haiku.db')
		self.cursor = self.connection.cursor()
		self.syllableCounter = SyllableCounter()

		path = "data/ngrams"

		self.fileList = [path+"/2grams.txt",
				path+"/3grams.txt",
				path+"/4grams.txt",
				path+"/5grams.txt"]
		
	def initialize(self):
		self.SyllableTablesInit()

	def SyllableTablesInit(self):
		self.cursor.execute('''CREATE TABLE FiveSyllables
					(id integer primary key, segment text)''')
		
		self.cursor.execute('''CREATE TABLE SevenSyllables
					(id integer primary key, segment text)''')
		
		#f = open("data/ngrams/5grams.txt")
		
		segmentList = {}
		
		count = 0
		for i in xrange(len(self.fileList)):
			f = open(self.fileList[i])
			for line in f:
				culledLine = " ".join([word.strip("\r\n") for word in line.split("\t")[1:(i+3)]])
				
				if culledLine.lower() not in segmentList:
					segmentList[culledLine.lower()] = 0
				else:
					continue
					
				syllableCounts = self.syllableCounter.getLineCounts(culledLine)
				
				if syllableCounts and syllableCounts[0] == 5:
					count+=1
					self.cursor.execute("INSERT into FiveSyllables VALUES (?,?)",(count,culledLine))

				if syllableCounts and syllableCounts[0] == 7:
					count+=1
					self.cursor.execute("INSERT into SevenSyllables VALUES (?,?)",(count,culledLine))
			
			self.connection.commit()
			f.close()		
		print count

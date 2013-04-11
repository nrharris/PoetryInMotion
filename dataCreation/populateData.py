import sqlite3
import csv
import re
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

		self.fiveCount = 0
		self.sevenCount = 0
		self.segmentList = {}
		self.posList = {}
		self.bigramList = {}
		self.conversion = {}

		for row in csv.reader(open("data/tagset/conversion.csv","rb")):
			self.conversion[row[0]] = row[1]

	def TablesInit(self):
		self.cursor.execute('''CREATE TABLE FiveSyllables
					(id integer primary key, segment text)''')
		
		self.cursor.execute('''CREATE TABLE SevenSyllables
					(id integer primary key, segment text)''')
		
		self.cursor.execute('''CREATE TABLE Bigrams
					(id integer primary key, firstWord text, firstPos text, secondWord text,
					secondPos text,frequency float, firstSyllables integer,secondSyllables integer)''')


		self.cursor.execute('''CREATE TABLE PoeticBigrams
					(firstWord text, firstPos text, secondWord text,
					secondPos text, firstSyllables integer,secondSyllables integer)''')

		self.PoeticBigrams()
	
		for i in xrange(len(self.fileList)):
			f = open(self.fileList[i])
			for line in f:
				self.SyllableTablesInit(line,i)

				if i == 3:  #only use 5grams data since using everything takes too long
					self.BuildBigramTable(line)

			self.connection.commit()
			f.close()
		
		self.BigramTablesInit()
		
	def SyllableTablesInit(self,line,fileNumber):
		#populates data in FiveSyllables Table and SevenSyllables Table
		    
		culledLine = " ".join([word.strip("\r\n") for word in line.split("\t")[1:(fileNumber+3)]])
				
		if culledLine.lower() not in self.segmentList:
			self.segmentList[culledLine.lower()] = 0
		else:
			return
					
		syllableCounts = self.syllableCounter.getLineCounts(culledLine)
				
		if syllableCounts and syllableCounts[0] == 5:
			self.fiveCount+=1
			self.cursor.execute("INSERT into FiveSyllables VALUES (?,?)",(self.fiveCount,culledLine))

		if syllableCounts and syllableCounts[0] == 7:
			self.sevenCount+=1
			self.cursor.execute("INSERT into SevenSyllables VALUES (?,?)",(self.sevenCount,culledLine))
			
		
	
	def BuildBigramTable(self,line):
		splitLine = [word.strip("\t\r\n ") for word in line.split("\t")]
		count = int(splitLine[0])

		for i in xrange(1,5):
			firstWord = splitLine[i]
			secondWord = splitLine[i+1]
			firstPos = self.convertPos(splitLine[i+5])
			secondPos = self.convertPos(splitLine[i+6])
			
			if firstWord not in self.bigramList:
				self.bigramList[firstWord] = {}
				self.bigramList[firstWord][secondWord] = []
				self.bigramList[firstWord][secondWord].append(firstPos)
				self.bigramList[firstWord][secondWord].append(secondPos)
				self.bigramList[firstWord][secondWord].append(count)
			else:
				if secondWord not in self.bigramList[firstWord]:
					self.bigramList[firstWord][secondWord] = []
					self.bigramList[firstWord][secondWord].append(firstPos)
					self.bigramList[firstWord][secondWord].append(secondPos)
					self.bigramList[firstWord][secondWord].append(count)
				else:
					self.bigramList[firstWord][secondWord][2]+=count
		
			if "totCount" not in self.bigramList[firstWord]:
				self.bigramList[firstWord]["totCount"] = count
			else:
				self.bigramList[firstWord]["totCount"]+=count
						
	def BigramTablesInit(self):
		count = 0
		for key,value in self.bigramList.items():
			for word,information in self.bigramList[key].items():
				if word != "totCount":
					count+=1
					keySyllables = self.syllableCounter.syllableCount(key) 
					wordSyllables = self.syllableCounter.syllableCount(word)

					information[2] = float("{0:.2f}".format(information[2]/(self.bigramList[key]["totCount"]+0.0)))
						
					self.cursor.execute("INSERT into Bigrams VALUES (?,?,?,?,?,?,?,?)",
								(count,key,information[0],word,information[1],information[2],
								 keySyllables,wordSyllables))

		self.connection.commit()

	def PoeticBigrams(self):

		f = open("data/haiku_samples/tagged_haiku")
		count = 0

		for line in f:
			splits = line.split(" ")
	
			if count % 3 == 0 or line == "\n":
				count += 1
				continue

			if count == 0 or count % 4 == 0:
				self.cursor.execute("INSERT into PoeticBigrams VALUES (?,?,?,?,?,?)",
							("S==>","S==>",splits[0].split("/")[0],splits[0].split("/")[1],
							 0,self.syllableCounter.syllableCount(splits[0].split("/")[0]),))
			else:
				for index in xrange(len(splits)-2):
					firstWord = splits[index].split("/")[0]
					secondWord = splits[index+1].split("/")[0]
					firstPos = splits[index].split("/")[1]
					secondPos = splits[index+1].split("/")[1]
					
					firstSyllables = self.syllableCounter.syllableCount(firstWord)
					secondSyllables = self.syllableCounter.syllableCount(secondWord)
					
					self.cursor.execute("INSERT into PoeticBigrams VALUES (?,?,?,?,?,?)",
								(firstWord,firstPos,secondWord,secondPos,firstSyllables,secondSyllables,))
					
			count+=1

	def convertPos(self,pos):
		pos = pos.upper()

		if pos in self.conversion:
			return self.conversion[pos]
		else:
			return pos
			












				

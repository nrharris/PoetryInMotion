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

		self.fiveCount = 0
		self.sevenCount = 0
		self.segmentList = {}
		self.posList = {}
		self.bigramList = {}

	def TablesInit(self):
		self.cursor.execute('''CREATE TABLE FiveSyllables
					(id integer primary key, segment text)''')
		
		self.cursor.execute('''CREATE TABLE SevenSyllables
					(id integer primary key, segment text)''')
		
		self.cursor.execute('''CREATE TABLE PosBigrams
					(id integer primary key, firstPOS text, secondPOS text, frequency float)''')
		
		self.cursor.execute('''CREATE TABLE Bigrams
					(id integer primary key, firstWord text, firstPos text, secondWord text,
					secondPos text,frequency float)''')


		
		for i in xrange(len(self.fileList)):
			f = open(self.fileList[i])
			for line in f:
				self.SyllableTablesInit(line,i)

				if i == 3:  #only use 5grams data since using everything takes too long
					self.BuildPosTable(line)
					self.BuildBigramTable(line)

			self.connection.commit()
			f.close()
		
		self.PosTablesInit()
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
			
		
	def BuildPosTable(self,line):
		'''
		   creates a dictionary of dictionaries
		   upper tier' keys denote the first part of speech
		   and lower tier keys represent parts of speech that follow.
		   values are the frequencies with which the pos pairings occur
		''' 
		splitLine = line.split("\t")
		count = int(splitLine[0])
		partsOfSpeech = [word.strip("\t\r\n") for word in splitLine[6:]] 	
		
		for i in range(len(partsOfSpeech)-1):
			pos = partsOfSpeech[i].strip("\t\r\n ")
			nextPos = partsOfSpeech[i+1].strip("\t\r\n ")

			if pos not in self.posList:
				self.posList[pos] = {}
				self.posList[pos][nextPos] = count
			else:
				if nextPos not in self.posList[pos]:
					self.posList[pos][nextPos] = count
				else:
					self.posList[pos][nextPos]+= count
			
			if "totSize" not in self.posList[pos]:
				self.posList[pos]["totSize"] = count
			else:
				self.posList[pos]["totSize"] += count
	
		#self.posSize+=count	
				
	def PosTablesInit(self):
		'''
		    takes the data created in BuildPosTable, 
		    normalizes the frequency, and inserts a copy of
		    the dictionary into the database	
		'''
		newPosList = {}
		
		for key,partsOfSpeech in self.posList.items():
			newPosList[key] = {}

			for pos,value in partsOfSpeech.items():
				if pos!="totSize":
					freq = (value/(self.posList[key]["totSize"]+0.0))
					
					if freq * 100 < 1:
						freq = .01
					else:
						freq = float("{0:.2f}".format(freq))

					newPosList[key][pos] = freq

		count = 0
		for key,partsOfSpeech in self.posList.items():
			for pos,value in partsOfSpeech.items():
				count+=1
				self.cursor.execute("INSERT into PosBigrams VALUES (?,?,?,?)",
						(count,key,pos,value))
		
		self.connection.commit()	

	
	def BuildBigramTable(self,line):
		splitLine = [word.strip("\t\r\n ") for word in line.split("\t")]
		count = int(splitLine[0])

		for i in xrange(1,5):
			firstWord = splitLine[i]
			secondWord = splitLine[i+1]
			firstPos = splitLine[i+5]
			secondPos = splitLine[i+6]
			
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
					information[2] = float("{0:.2f}".format(information[2]/(self.bigramList[key]["totCount"]+0.0)))
					
					self.cursor.execute("INSERT into Bigrams VALUES (?,?,?,?,?,?)",
								(count,key,information[0],word,information[1],information[2]))

					#print key + " " + word + " " + information[0] + " " + information[1]
		self.connection.commit()
		#print self.bigramList	



















				

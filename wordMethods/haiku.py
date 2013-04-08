from wordMethods.sounds import SyllableCounter
from evolution.mutate import mutate, fitness
from wordMethods.partsOfSpeech import pos
from random import randint
import sqlite3

def isHaiku(text):
	sc = SyllableCounter()
	counts = sc.getLineCounts(text)
	expectedCounts = [5,7,5]
	
	if not counts:
		return False

	if len(counts) != 3:
		return False

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

	haiku = []
	
	cursor.execute("select segment from FiveSyllables where id = ?",(firstIndex,))
	haiku.append(cursor.fetchone()[0])
	cursor.execute("select segment from SevenSyllables where id = ?",(secondIndex,))
	haiku.append(cursor.fetchone()[0])
	cursor.execute("select segment from FiveSyllables where id = ?",(thirdIndex,))
	haiku.append(cursor.fetchone()[0])
	
	connection.close()
	return "\n".join(haiku)

def createEvolvedHaiku():
	initialHaiku = createNaiveHaiku()
	
	fitnessLevel = fitness(initialHaiku)

	bestHaiku = initialHaiku
	bestFitness = fitnessLevel
	
	count = 0
	for i in xrange(2000):
		count+=1
		initialHaiku = mutate(initialHaiku)
		fitnessLevel = fitness(initialHaiku)
		
		if fitnessLevel > bestFitness:
			bestHaiku = initialHaiku
			bestFitness = fitnessLevel

		print initialHaiku  + "\n"
		print "count is: " + str(count)

	print "Best Haiku is :\n"+bestHaiku
	print "\nEvaluation is:\n" + str(bestFitness)
	print pos(bestHaiku)

def grammarHaiku():
	sc = SyllableCounter()
	grammar = [["NN", "NN"],
		   ["DT", "NN","IN","DT","NN"], 
		   ["NNS", "IN","DT","NN"]]			
	
	newGrammar = [[None]*len(grammar[0]),
		      [None]*len(grammar[1]),
		      [None]*len(grammar[2])] 

	connection = sqlite3.connect('data/haiku.db')
	cursor = connection.cursor()
	
	lengths = [0,0,0]
	expectedLengths = [5,7,5]

	lineNum = 0
	

	for line in xrange(len(grammar)):
		someLine = ""
		
		index = 0
			
		while index < len(grammar[line]):
			if index == 0:
				wordList = [row for row in 
					cursor.execute("select firstWord,secondWord from PoeticBigrams where firstPos =? and secondPos =?",
					(grammar[line][index],grammar[line][index+1],))]
				
				randomIndex = int(randint(0,len(wordList)-1))
				newGrammar[line][index] = str(wordList[randomIndex][0])
				newGrammar[line][index+1] = str(wordList[randomIndex][1])
				
				index +=2
				continue 
			else:
				wordList = [row for row in 
					cursor.execute("select secondWord from PoeticBigrams where firstWord = ? and secondPos = ?",
					(newGrammar[line][index-1],grammar[line][index],))]
				
				if len(wordList) == 0:
					wordList = [row for row in
					cursor.execute("select secondWord from PoeticBigrams where firstPos = ? and secondPos = ?",
					(grammar[line][index-1],grammar[line][index],))]
					
				randomIndex = int(randint(0,len(wordList)-1))

				newGrammar[line][index] = str(wordList[randomIndex][0])
				
			index+=1

	print "\n".join([" ".join(line) for line in [line for line in newGrammar]])

from wordMethods.sounds import SyllableCounter
from evolution.mutate import Individual
from random import randint
import sqlite3
import string

class Haiku:

	def __init__(self):
		self.syllableCounter = SyllableCounter()
		self.grammar = self.setGrammar()
			
	def isHaiku(self,text):
		counts = self.syllableCounter.getLineCounts(text)
		expectedCounts = [5,7,5]
	
		if not counts:
			return False

		if len(counts) != 3:
			return False

		for i in xrange(len(expectedCounts)):
			if counts[i] != expectedCounts[i]:
				return False

		return True	

	def createNaiveHaiku(self):
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

	def createEvolvedHaiku(self):
		individual = Individual(self.grammar)
		initialHaiku = self.createNaiveHaiku()
	
		fitnessLevel = individual.fitness(initialHaiku)

		bestHaiku = initialHaiku
		bestFitness = fitnessLevel
	
		for i in xrange(5000):
			initialHaiku = individual.naiveMutate(initialHaiku)
			fitnessLevel = individual.fitness(initialHaiku)
		
			if fitnessLevel > bestFitness:
				bestHaiku = initialHaiku
				bestFitness = fitnessLevel

			print initialHaiku  + "\n"
			print "count is: " + str(i)

		print "Best Haiku is :\n"+bestHaiku
		print "\nEvaluation is:\n" + str(bestFitness)

	def grammarHaiku(self):
		grammar = self.grammar
		newGrammar = [[None]*len(grammar[0]),
			      [None]*len(grammar[1]),
		      	      [None]*len(grammar[2])] 

		connection = sqlite3.connect('data/haiku.db')
		cursor = connection.cursor()
	
		for line in xrange(len(grammar)):
		
			for index in xrange(len(grammar[line])):
				if grammar[line][index] in string.punctuation:
					newGrammar[line][index] = grammar[line][index]
					continue

				if index == 0:
					query = "select firstWord,secondWord from PoeticBigrams where firstPos=? and secondPos=?"
					
					wordList = [row for row in 
						cursor.execute(query,(grammar[line][index],grammar[line][index+1],))]
					
					if len(wordList) == 0:
						query = "select firstWord from PoeticBigrams where firstPos=?"
						wordList = [row for row in cursor.execute(query,(grammar[line][index],))]
						randomIndex = int(randint(0,len(wordList)-1))
						newGrammar[line][index] = str(wordList[randomIndex][0])
						continue
								
					randomIndex = int(randint(0,len(wordList)-1))
					newGrammar[line][index] = str(wordList[randomIndex][0])
					newGrammar[line][index+1] = str(wordList[randomIndex][1])
				
					index +=1
					continue 
				else:
					wordList = [row for row in 
						cursor.execute("select secondWord from PoeticBigrams where firstWord = ? and secondPos = ?",
						(newGrammar[line][index-1],grammar[line][index],))]
				
					if len(wordList) == 0:
						wordList = [row for row in
						cursor.execute("select secondWord from PoeticBigrams where firstPos = ? and secondPos = ?",
						(grammar[line][index-1],grammar[line][index],))]
				
					if len(wordList) == 0:
						wordList = [row for row in 
						cursor.execute("select firstWord from PoeticBigrams where firstPos = ?",
						(grammar[line][index],))]
	
					randomIndex = int(randint(0,len(wordList)-1))

					newGrammar[line][index] = str(wordList[randomIndex][0])
				

		return "\n".join([" ".join(line) for line in [line for line in newGrammar]])
	
	def setGrammar(self):
		count = 0
		grammar = ""
		grammars = []

		for line in open("data/haiku_grammar/grammar"):
			count+=1
			if count%4==0:
				grammars.append(grammar)
				grammar = ""
			grammar+=line
		
		randIndex = int(randint(0,len(grammars)-1))
		
		newGrammars = []
			
		if len(grammars[randIndex].splitlines()[0]) > 1:
			splitLines = grammars[randIndex].splitlines()
		else:
			splitLines = grammars[randIndex].splitlines()[1:]

		for line in splitLines:
			newGrammars.append(line.split(" "))
		
		return newGrammars

	def getGrammar(self):
		return self.grammar

	def evolvedGrammarHaiku(self):
	
		bestHaiku = ""
		bestFitness = 0
		currFitness = 0
	
		individual = Individual(self.grammar)

		for i in xrange(5000):
			newHaiku = self.grammarHaiku()
			currFitness = individual.fitness(newHaiku)
			
			if currFitness != 0:
				print newHaiku
				print individual.mutate(newHaiku)
				print currFitness
				print "\n"

			if currFitness > bestFitness:
				bestHaiku = newHaiku
				bestFitness = currFitness
		
		print "Best haiku is:"
		print bestHaiku
		print bestFitness		
		print self.grammar	
		

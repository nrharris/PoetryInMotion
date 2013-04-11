from wordMethods.sounds import SyllableCounter
from nltk.corpus import wordnet as wn
from random import randint
from random import choice
import sqlite3
import itertools

class Individual:
	
	def __init__(self):
		self.syllableCounter = SyllableCounter()
	
	def naiveMutate(self,haiku):
		connection = sqlite3.connect("data/haiku.db")
		cursor = connection.cursor()
	
		lines = haiku.split("\n")	
	
		randomSelection = randint(1,11)
	
		if randomSelection < 6:
			cursor.execute("Select count(*) from FiveSyllables")
			fiveUpperBound = cursor.fetchone()[0]
			randomIndex = int(randint(0,fiveUpperBound))
			cursor.execute("Select segment from FiveSyllables where id = ?",(randomIndex,))
		
			randomLine = choice([0,2])
			lines[randomLine] = cursor.fetchone()[0]
		else:
			cursor.execute("Select count(*) from SevenSyllables")
			sevenUpperBound = cursor.fetchone()[0]
			randomIndex = int(randint(0,sevenUpperBound))
			cursor.execute("Select segment from SevenSyllables where id = ?",(randomIndex,))
			lines[1] = cursor.fetchone()[0]	
	
		return "\n".join(lines)

	
	def fitness(self,haiku):
		splits = [line.split(" ") for line in haiku.split("\n")]	
		words = [str(word) for word in list(itertools.chain(*splits))]
 	
		similarity = 0	

		for word in words:
			if wn.morphy(word,wn.NOUN):
				nounSyns = wn.synsets(word,wn.NOUN)

				for secondWord in words:
					if wn.morphy(secondWord,wn.NOUN) and word!=secondWord:
						for synset in nounSyns:
							if secondWord in synset.lemma_names:
								similarity+=10
		similarity+=self.isHaiku(haiku)
			
		#print similarity	
		return similarity


	def isHaiku(self,haiku):	
		
		haikuCounts = [5,7,5]
		lineCounts = []
		splits = [line.split(" ") for line in haiku.split("\n")]	
 		
		for line in splits:
			count = 0
			for word in line:	
				count += self.syllableCounter.syllableCount(word)
			
			lineCounts.append(count)
	
		if haikuCounts == lineCounts:
			return 200
		else:
			return 0

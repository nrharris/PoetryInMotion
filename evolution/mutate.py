from wordMethods.sounds import SyllableCounter
from associations.associations import *
from associations.Seasons import *
from nltk.corpus import wordnet as wn
from random import randint,choice
import sqlite3
import itertools

class Individual:
	
	def __init__(self,grammar,season):
		self.syllableCounter = SyllableCounter()
		self.grammar = grammar
		self.season = season
	
		connection = sqlite3.connect("data/haiku.db")
		self.cursor = connection.cursor()

	def naiveMutate(self,haiku):
	
		lines = haiku.split("\n")	
	
		randomSelection = randint(1,11)
	
		if randomSelection < 6:
			self.cursor.execute("Select count(*) from FiveSyllables")
			fiveUpperBound = self.cursor.fetchone()[0]
			randomIndex = int(randint(0,fiveUpperBound))
			self.cursor.execute("Select segment from FiveSyllables where id = ?",(randomIndex,))
		
			randomLine = choice([0,2])
			lines[randomLine] = self.cursor.fetchone()[0]
		else:
			self.cursor.execute("Select count(*) from SevenSyllables")
			sevenUpperBound = self.cursor.fetchone()[0]
			randomIndex = int(randint(0,sevenUpperBound))
			self.cursor.execute("Select segment from SevenSyllables where id = ?",(randomIndex,))
			lines[1] = self.cursor.fetchone()[0]	
	
		return "\n".join(lines)

	def mutate(self,haiku):
		splitHaiku = [line.split(" ") for line in [line for line in haiku.splitlines()]]				
		
		seasonList = {"summer": Summer(),"winter": Winter(),"fall": Fall(),"spring": Spring()}
		
		associations = seasonList[self.season]
			
		splitHaiku = self.replaceNouns(splitHaiku,associations)
		
		return "\n".join([" ".join(line) for line in [line for line in splitHaiku]])

	def replaceNouns(self,splitHaiku,seed):

		for i in xrange(len(splitHaiku)):
			for j in xrange(len(splitHaiku[i])):
				if "NN" in self.grammar[i][j] and splitHaiku[i][j] != seed:
					
					if len(seed) == 0:
						break
					
					replacement = seed[randint(0,len(seed)-1)]
					seed.remove(replacement)
					
					if j != 0:
						pre = [row for row in self.cursor.execute('''select firstWord from Bigrams 
						where firstPos = ? and secondWord =?''',
						(self.grammar[i][j-1],replacement))]
						
						if len(pre) > 0:
							index = randint(0,len(pre)-1)
							splitHaiku[i][j-1] = str(pre[index][0])

					if j < len(splitHaiku[i])-1:
						pos = [row for row in self.cursor.execute('''select secondWord from Bigrams
						where secondPos = ? and firstWord = ?''',
						(self.grammar[i][j+1],replacement))]
					
						if len(pos) > 0:
							index = randint(0,len(pos)-1)
							splitHaiku[i][j+1] = str(pos[index][0])

					splitHaiku[i][j] = replacement

		return splitHaiku		
	
		
	def fitness(self,haiku):
		splits = [line.split(" ") for line in haiku.split("\n")]	
		words = [str(word) for word in list(itertools.chain(*splits))]
 	
		similarity = 0	

		for word in words:
			if wn.morphy(word,wn.NOUN):
				nounSyns = wn.synsets(word,wn.NOUN)

				for secondWord in words:
					if wn.morphy(secondWord,wn.NOUN) and (word not in secondWord and secondWord not in word):
						for synset in nounSyns:
							if secondWord in synset.lemma_names:
								#similarity+=10
								pass

					similarity+=connectedness(word,secondWord)					

						
		similarity+=self.isHaiku(haiku)
			
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

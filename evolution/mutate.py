from wordMethods.sounds import SyllableCounter
from associations.associations import randomWalk
from associations.Seasons import Winter
from nltk.corpus import wordnet as wn
from random import randint
from random import choice
import sqlite3
import itertools

class Individual:
	
	def __init__(self,grammar):
		self.syllableCounter = SyllableCounter()
		self.grammar = grammar

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

	def mutate(self,haiku):
		splitHaiku = [line.split(" ") for line in [line for line in haiku.splitlines()]]				

		associations = Winter()
			
		splitHaiku = self.replaceNouns(splitHaiku,associations)

		return "\n".join([" ".join(line) for line in [line for line in splitHaiku]])

	def replaceNouns(self,splitHaiku,seed):
		connection = sqlite3.connect("data/haiku.db")
		cursor = connection.cursor()

		for i in xrange(len(splitHaiku)):
			for j in xrange(len(splitHaiku[i])):
				if "NN" in self.grammar[i][j] and splitHaiku[i][j] != seed:
					if len(seed) == 0:
						break

					replacement = seed[randint(0,len(seed[1])-1)]
					seed.remove(replacement)
					
					if j != 0:
						pre = [row for row in cursor.execute('''select firstWord from Bigrams 
						where firstPos = ? and secondWord =?''',
						(self.grammar[i][j-1],replacement))]
						
						if len(pre) > 0:
							index = randint(0,len(pre)-1)
							splitHaiku[i][j-1] = str(pre[index][0])

					if j < len(splitHaiku[i])-1:
						pos = [row for row in cursor.execute('''select secondWord from Bigrams
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

from wordMethods.sounds import SyllableCounter
from nltk.corpus import wordnet as wn
from random import randint
from random import choice
import sqlite3
import itertools

def mutate(haiku):
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

def fitness(haiku):
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
 	
	similarity = 0
	treeSet = wn.synsets("tree",wn.NOUN)[0]
	
	for word in words:
		if wn.morphy(word,wn.NOUN):
			noun = wn.synsets(word,wn.NOUN)[0]
			if similarity < treeSet.path_similarity(noun):
				similarity = treeSet.path_similarity(noun)
	print similarity			
	#return (6/(len(words)+0.0)) * 100 
	return similarity

'''def fitness(haiku):
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
	print (6/(len(words)+0.0)) * 100 
	
	return (6/(len(words)+0.0)) * 100 '''

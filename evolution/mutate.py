from wordMethods.sounds import SyllableCounter
from wordMethods.partsOfSpeech import pos
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
	
	wordPos = pos(haiku)	
	
	nouns = [thing for thing in wordPos if 'nn' in thing[1]]
	
	for noun in nouns:
		if wn.morphy(noun[0],wn.NOUN):
			nounSyns = wn.synsets(noun[0],wn.NOUN)

			for comparedNoun in nouns:
				if wn.morphy(comparedNoun[0],wn.NOUN) and comparedNoun[2]!=noun[2]:
					for synset in nounSyns:
						if comparedNoun[0] in synset.lemma_names:
							similarity+=10				
	
	size = (6/(len(words)+0.0))
	score = similarity*size
	
	if score < .01:
		score = size
	
	print score
	return score
	
'''def fitness(haiku):
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
	print (6/(len(words)+0.0)) * 100 
	
	return (6/(len(words)+0.0)) * 100 '''

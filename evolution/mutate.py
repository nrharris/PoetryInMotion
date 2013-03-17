from wordMethods.sounds import SyllableCounter
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
	
 	
	#splits = [line.split(" ") for line in haiku.split("\n")]	
	#words = [str(word) for word in list(itertools.chain(*splits))]
	
		

def fitness(haiku):
	score = 0

	firstLetter = haiku[0]
	
	if ord(firstLetter.capitalize()) == ord(firstLetter):
		score += 100
	
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
	
	for word in [word.lower() for word in words]:
		if word[0] == 'a':
			score+=75


	return score
 

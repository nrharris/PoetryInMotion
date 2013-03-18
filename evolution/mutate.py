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
	
 			

def fitness(haiku):
	#variable declaration
	connection = sqlite3.connect("data/haiku.db")
	cursor = connection.cursor()

	score = 0
	
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
	
	#First word capitalized, logical sentence start	
	firstLetter = haiku[0]	
	if ord(firstLetter.capitalize()) == ord(firstLetter):
		score += 200
	
	#First and second lines are likely to provide some continuity
	firstWord = splits[0][-1]
	secondWord = splits[1][0]

	cursor.execute("select count(*) from Bigrams where firstWord = ? and secondWord = ?",(firstWord,secondWord,))
			
	count = cursor.fetchone()[0] 
	if count > 0:
		score+=100
		
	#Grammatically correct sentence endings
	secondLinePrec = splits[1][-2]
	secondLineEnd = splits[1][-1]
	cursor.execute("select secondPos from Bigrams where firstWord = ? and secondWord = ?", (secondLinePrec,secondLineEnd,))
	
	try:
		secondLinePos = cursor.fetchone()[0].lower()
		if secondLinePos[0] != 'd' and secondLinePos[0] != 'v':
			score+=100
	except:
		pass

	finalLinePrec = splits[2][-2]
	finalLineEnd = splits[2][-1]
	cursor.execute("select secondPos from Bigrams where firstWord = ? and secondWord = ?",(finalLinePrec, finalLineEnd,))
	
	try:
		finalLinePos = cursor.fetchone()[0].lower()
		if finalLinePos[0] != 'd' and finalLinePos[0] != 'v':
			score+=100
	except:
		pass

	#Third line capitalized, creates juxtaposition
	thirdStart = splits[2][0][0]

	if ord(thirdStart.capitalize()) == ord(thirdStart):
		score += 200


	return score
 

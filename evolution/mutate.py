from wordMethods.sounds import SyllableCounter
from random import randint
import sqlite3
import itertools

def mutate(haiku):
	connection = sqlite3.connect("data/haiku.db")
	cursor = connection.cursor()
	
	splits = [line.split(" ") for line in haiku.split("\n")]	
	words = [str(word) for word in list(itertools.chain(*splits))]
	
	mutationFound = False
	
	while not mutationFound:
		randomIndex = randint(0,len(words)-1)
	
		if randomIndex == 0:
			cursor.execute("Select firstWord from Bigrams where secondWord = ?",([words[randomIndex+1]]))
			try:
				replacementWord = cursor.fetchone()[0]
				mutationFound = True
			except:
				continue	

		elif randomIndex  == len(words)-1:
			cursor.execute("Select secondWord from Bigrams where firstWord = ?", ([words[randomIndex-1]]))
			try:
				replacementWord = cursor.fetchone()[0]
				mutationFound = True
			except:
				continue		
		else:
			cursor.execute("Select firstWord from Bigrams where secondWord = ?",([words[randomIndex+1]]))
			try:
				middleWord = cursor.fetchone()[0]
				mutationFound = True
			except:
				continue
			cursor.execute("Select count(*) from Bigrams where firstWord = ? and secondWord = ?",(words[randomIndex-1],middleWord))
			count = cursor.fetchone()[0]
			
			if count == 0:
				mutationFound = False
				continue

			replacementWord = middleWord
		
	
	return haiku.replace(words[randomIndex],replacementWord)

def fitness(haiku):
	return 0 

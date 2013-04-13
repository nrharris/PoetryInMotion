import sqlite3
from random import randint
from random import choice

def randomWalk(seed):
	conn = sqlite3.connect("data/haiku.db")
	cursor = conn.cursor()
	walkedList = []
	
	cursor.execute("select count(*) from WordAssociations where cue = ? or target = ?", (seed,seed,))
	
	if cursor.fetchone()[0] == 0:
		return walkedList

	for i in xrange(8):
		randirection = choice([1,2])
		
		choices = []
		
		count = 0
	
		while len(choices) == 0:
			if count == 10:
				return walkedList
			if randirection == 1:
				choices = [row for row in 
					cursor.execute("select target from WordAssociations where cue = ? and FSG>=.03", (seed,))]
			else:
				choices = [row for row in 
					cursor.execute("select cue from WordAssociations where target = ? and BSG>=.03", (seed,))]
			
			count+=1

		index = randint(0,len(choices)-1)
		seed = str(choices[index][0])
		walkedList.append(seed)
	
	return walkedList



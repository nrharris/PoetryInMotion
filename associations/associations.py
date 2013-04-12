import sqlite3
from random import randint
from random import choice

def randomWalk(seed):
	conn = sqlite3.connect("data/haiku.db")
	cursor = conn.cursor()
	
	for i in xrange(8):
		randirection = choice([1,2])
		
		if randirection == 1:
			choices = [row for row in 
				cursor.execute("select target from WordAssociations where cue = ?", (seed,))]
		else:
			choices = [row for row in 
				cursor.execute("select cue from WordAssociations where target = ?", (seed,))]
			
		index = randint(0,len(choices)-1)
		seed = str(choices[index][0])
		print seed


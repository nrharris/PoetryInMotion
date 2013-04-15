from wordMethods.haiku import Haiku
import sys

def naive(haiku):
	return haiku.createEvolvedHaiku()

def grammar(haiku):
	haiku.evolvedGrammarHaiku()

def init():
	from dataCreation.populateData import DatabaseInit
	d = DatabaseInit()
	d.TablesInit()

def redditAll():
	from reddit.worker import Reddit
	r = Reddit()
	r.allComments()

def redditSub(sub):
	from reddit.worker import Reddit
	r = Reddit()
	r.subredditComments(sub)
	
def unknown():
	print "Unknown command"

if __name__ == "__main__":
	
	haiku = Haiku()
	
	if len(sys.argv) > 1:
		
		commands = ["naive","grammar","init","reddit"]

		if sys.argv[1].lower() == "naive":
			naive(haiku)
		
		if sys.argv[1].lower() == "grammar":
			grammar(haiku)
		
		if sys.argv[1].lower() == "init":
			init()
		
		if sys.argv[1].lower() == "reddit":
			
			if len(sys.argv) == 3:
				redditSub(sys.argv[2].lower())
			else:
				redditAll()
		
		if sys.argv[1].lower() not in commands:
			print "Unknown command"

	else:
		naive(haiku)	
			

from sounds import SyllableCounter
from random import randint

def isHaiku(text):
	sc = SyllableCounter()
	counts = sc.getLineCounts(text)
	expectedCounts = [5,7,5]
	
	if not counts:
		return False

	if len(counts) != 3:
		return false

	for i in xrange(len(expectedCounts)):
		if counts[i] != expectedCounts[i]:
			return False

	return True	

def createNaiveHaiku():
	f = open("../experimentalCode/ngrams/5grams.txt","r")
	sc = SyllableCounter()	
	
	fiveCounts = []
	sevenCounts = []

	for line in f:
		count = 0
		words = line.split("\t")
		
		for i in xrange(1,6):
			count += sc.syllableCount(words[i])
		
		if count == 5:
			fiveCounts.append(" ".join(words[1:6]))

		if count == 7:
			sevenCounts.append(" ".join(words[1:6]))	
		
	print fiveCounts[randint(0,len(fiveCounts)-1)]
	print sevenCounts[randint(0,len(sevenCounts)-1)]
	print fiveCounts[randint(0,len(fiveCounts)-1)]

createNaiveHaiku()

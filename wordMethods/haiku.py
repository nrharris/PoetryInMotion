from sounds import SyllableCounter

def isHaiku(text):
	sc = SyllableCounter()
	counts = sc.getLineCounts(text)
	expectedCounts = [5,7,5]
	
	if len(counts) != 3:
		return false

	for i in xrange(len(expectedCounts)):
		if counts[i] != expectedCounts[i]:
			return False

	return True	
	

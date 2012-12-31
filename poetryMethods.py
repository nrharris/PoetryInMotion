import nltk

pronunciationDict = nltk.corpus.cmudict.dict()

def rhymes(firstWord,secondWord):	
	#returns true if a firstWord rhymes with secondWord
	#Currently only works with last syllable rhyming
	
	for fword in pronunciationDict[firstWord]:
		for sword in pronunciationDict[secondWord]:
			if fword[-1] == sword[-1]:
				return True
	return False

def generateRhymingWords(word):
	#returns a list of words rhyming with word
	#obviously horribly inefficient

	suffixes = set([wordv[-1] for wordv in pronunciationDict[word]])
	rhymingWords = []
	for eachWord in pronunciationDict:
		for wordSuffix in pronunciationDict[eachWord]:
			if wordSuffix[-1] in suffixes:
				rhymingWords.append(eachWord)
	return rhymingWords


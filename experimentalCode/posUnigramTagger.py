fileList = []

fileList.append(open("ngrams/5grams.txt","r"))
fileList.append(open("ngrams/4grams.txt","r"))
fileList.append(open("ngrams/3grams.txt","r"))
fileList.append(open("ngrams/2grams.txt","r"))

c = {}

fileRange = 5

for f in fileList:
	for line in f:
		words = line.split("\t")
		for i in xrange(1,fileRange):
			if not c.get(words[i].lower()):
				c[words[i].lower()] = [words[i+fileRange].strip('\n\r\t')]
			else:
				c[words[i].lower()].append(words[i+fileRange].strip('\t\r\n'))
	
	fileRange-=1
	f.close()

posFrequencies = {}

for word in c:
	posSet = frozenset(c[word])
	posLen = len(c[word]) + 0.0
	freqs = zip(posSet,[c[word].count(POS)/posLen for POS in posSet])
	posFrequencies[word] = freqs

del c

def printPartsOfSpeech(text,posFrequencies):

	for word in text.split(" "):
		tempWord = ""
		freq = 0
		for count in posFrequencies[word.lower()]:
			someWord,percent = count
			if (percent * 100) > freq:
				tempWord = someWord
				freq = percent * 100

		print word + " " + tempWord + " "  + str(freq)

testString = "What string would you like me to test"			 		
printPartsOfSpeech(testString,posFrequencies)

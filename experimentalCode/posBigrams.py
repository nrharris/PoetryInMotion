f = open("ngrams/5grams.txt")

posFrequencies = {}

for line in f:
	tokens = line.split("\t")
	
	for i in range(6,10):
		tokens[i] = tokens[i].strip("\t\r\n")
		tokens[i+1] = tokens[i+1].strip("\t\r\n")

		if tokens[i] not in posFrequencies:
			posFrequencies[tokens[i]] = []
			posFrequencies[tokens[i]].append(tokens[i+1])
		else:
			posFrequencies[tokens[i]].append(tokens[i+1])

newPosFrequencies = {}

for word in posFrequencies:
	newPosFrequencies[word] = []

	for pos in set(posFrequencies[word]):
		posCount = posFrequencies[word].count(pos)
		totLength = len(posFrequencies[word])+0.0

		newPosFrequencies[word].append((pos,posCount/totLength))


def highestFreq(tupleList):
	
	pairedList = []

	for word,freq in tupleList:
		if (freq * 100) > 10:
			pairedList.append((word,freq))

	return pairedList

for word in newPosFrequencies:
	print word
	print highestFreq(newPosFrequencies[word])


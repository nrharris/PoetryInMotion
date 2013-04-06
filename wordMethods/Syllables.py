import nltk

class SyllableCounter():

	def __init__(self):
		self.pronunciationDict = nltk.corpus.cmudict.dict()
	
	def getLineCounts(self,words):
		#returns cumulative syllable counts of each line
		lines = words.splitlines()
		
		lineCounts = []
			
		for line in lines:
			count = 0
			for word in line.split(" "):
				word = word.strip(",-!?.;: ")
				if len(word)==0:
					break
				if word.lower() not in self.pronunciationDict:
					return False
				count+=self.syllableCount(word.lower())
			lineCounts.append(count)
		return lineCounts
		
	def syllableCount(self,word):
		#returns syllable count of a single word
		count = 0
		word = word.lower()
	
		if word not in self.pronunciationDict:
			return 0
	
		for syllable in self.pronunciationDict[word][0]:
			if syllable[-1].isdigit():
				count+=1 
		return count

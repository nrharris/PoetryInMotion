import nltk
import re

class Rhymer():

	def __init__(self):
		self.pronunciationDict = nltk.corpus.cmudict.dict()

	def lastStressed(self,word):
		index = len(word)-1
		pattern = re.compile("[1-9]")

		for i in reversed(range(len(word))):
			if pattern.search(word[i]):
				return i
		return index

	def rhymes(self,firstWord,secondWord):
		firstWord = firstWord.lower()
		secondWord = secondWord.lower()	
		for pronunciation in self.pronunciationDict[firstWord]:
			index = self.lastStressed(pronunciation)
			for pronun in self.pronunciationDict[secondWord]:
				if pronun[index:] == pronunciation[index:]:
					return True		
		return False

	def generateRhymingWords(self,word):
		wordList = []
		word = word.lower()
		for rword in self.pronunciationDict:
			if self.rhymes(word,rword) and word!=rword:
				wordList.append(rword)
		return wordList


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
		word = word.lower()
    
		if word not in self.pronunciationDict:
     			return -100
               
      		return len([syllable for syllable in self.pronunciationDict[word][0] if syllable[-1].isdigit()])

'''sc = SyllableCounter()
diction = nltk.corpus.cmudict.dict()

print diction["fire"]
print sc.syllableCount("fire")

print "pin"
print diction["pin"]
print sc.syllableCount("pin") 

print "pen"
print diction["pen"]
print sc.syllableCount("pen")

print "alligator"
print diction["alligator"]
print sc.syllableCount("alligator")

print "antidisestablishmentarianism"
print diction["antidisestablishmentarianism"]
print sc.syllableCount("antidisestablishmentarianism")

print sc.syllableCount("windchimes")
'''


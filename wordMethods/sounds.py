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
		lines = words.split("\n")
		lineCounts = []
		
		for line in lines:
			count = 0
			for word in line.split(" "):
				count+=self.syllableCount(word)
			lineCounts.append(count)
		return lineCounts
		
	def syllableCount(self,word):
		#returns syllable count of a single word
		count = 0
		word = word.lower()
		
		for syllable in self.pronunciationDict[word][0]:
			if syllable[-1].isdigit():
				count+=1 
		return count


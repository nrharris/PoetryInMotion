import nltk
import re

class Rhymer():
	#Rhymer deals with words and their sounds

	def __init__(self):
		self.pronunciationDict = nltk.corpus.cmudict.dict()

	def lastStressed(self,word):
		#returns the index of the lass stressed syllable
		#expects a list of syllables
		
		index = len(word)-1
		pattern = re.compile("[1-9]")

		for i in reversed(range(len(word))):
			if pattern.search(word[i]):
				return i
		return index

	def rhymes(self,firstWord,secondWord):	
		#returns true if a firstWord rhymes with secondWord
		#only returns perfect rhymes
				
		for pronunciation in self.pronunciationDict[firstWord]:
			index = self.lastStressed(pronunciation)
			for pronun in self.pronunciationDict[secondWord]:
				if pronun[index:] == pronunciation[index:]:
					return True		
		return False

	def generateRhymingWords(self,word):
		#returns a list of words rhyming with word
		
		wordList = []
		for rword in self.pronunciationDict:
			if self.rhymes(word,rword):
				wordList.append(rword)
		return wordList


import praw
from wordMethods.haiku import Haiku
from wordMethods.sounds import SyllableCounter
import itertools

class Reddit:
	
	def __init__(self):
		self.agent = praw.Reddit(user_agent="cs_haiku_bot")
		self.haiku = Haiku()
		self.sc = SyllableCounter()

	def allComments(self):
		for comment in [x.body for x in self.agent.get_all_comments(limit=300)]:
			if self.sc.getLineCounts(comment) and sum(self.sc.getLineCounts(comment)) == 17:
				print "haiku found"
				self.prepareHaiku(comment)

	def prepareHaiku(self,comment):
		lineCounts = [5,7,5]
		
		splits = [line.split(" ") for line in comment.splitlines()]	
		words = [str(word) for word in list(itertools.chain(*splits))]
		
		count = 0
		lineIndex = 0
		haiku = ""
		
		print "Comment: \n"
		print comment

		for index in xrange(len(words)):
			if count == lineCounts[lineIndex]:
				haiku+="\n"
				haiku+=words[index] + " "
				count = self.sc.syllableCount(words[index])
				lineIndex+=1
				print lineIndex
			else:
				haiku+=words[index] + " "
				count += self.sc.syllableCount(words[index])
		
		print "Haiku: \n"
		print haiku
								

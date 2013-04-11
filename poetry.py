from wordMethods.haiku import Haiku

haiku = Haiku()
haiku.evolvedGrammarHaiku()

'''
haiku = "" 
count = 0
haikuChecker = Haiku()

for line in open("data/haiku_samples/tagged_haiku"):
	if len(line) == 1:
		continue
	
	if count%4==0:
		grammar = ""
		words = ""
		for lines in haiku.splitlines():
			grammar += " ".join([word.split("/")[1] for word in lines.split(" ") if len(word.split("/")) > 1])+"\n"
			words += " ".join([word.split("/")[0] for word in lines.split(" ") if len(word.split("/")) > 0])+"\n"
		
		if haikuChecker.isHaiku(words):
			print grammar

		#print haiku
		haiku=""
		count+=1
		continue
		
	count+=1	
	haiku+=line
'''

from associations import randomWalk

def Winter():
	words = []
	seedList = ["snow","shadow","barren","cold","chill","ice","frozen","alone"]
	
	for seed in seedList:
		for word in randomWalk(seed):
			words.append(word)
	
	return words

def Summer():
	
	words = []
	seedList = ["sun","hot","breeze","warm","shade","beach","relax"]
	
	for seed in seedList:
		for word in randomWalk(seed):
			words.append(word)
	
	return words
	
def Fall():
	
	words = []
	seedList = ["autumn","leaf","brown","chestnut","rake","scarecrow","seeds","stuffing"]
	
	for seed in seedList:
		for word in randomWalk(seed):
			words.append(word)
	
	return words

def Spring():
	
	words = []
	seedList = ["flowers","rain","rainbow","new","grass","butterfly"]
	
	for seed in seedList:
		for word in randomWalk(seed):
			words.append(word)
	
	return words



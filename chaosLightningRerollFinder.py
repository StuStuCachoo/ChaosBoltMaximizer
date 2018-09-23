from random import randrange

def roll(level, maxRolls, rerollValues):
	d1 = randrange(1,9,1)
	d2 = randrange(1,9,1)
	final = 0
	for i in range(0,level):
		final += randrange(1,7,1)
	rerolls = maxRolls
	while rerolls > 0 or d1==d2:
		#print(f"{d1},{d2},{rerolls},{final}")
		if(d1 != d2):
			if(d1 > rerollValues[rerolls-1] and d2 > rerollValues[rerolls-1]):
				break;
			elif(d1 < d2):
				d1 = randrange(1,9,1)
			else:
				d2 = randrange(1,9,1)
			rerolls -= 1
		else:
			final += d1 + d2
			for i in range(0,level):
				final += randrange(1,7,1)
			d1 = randrange(1,9,1)
			d2 = randrange(1,9,1)
	final += d1 + d2
	return final

def simRolls(level, maxRolls):
	allArrays = rerollArrays(5,8,maxRolls)
	for i in range(len(allArrays)):
		sum = 0
		for j in range(100000):
			sum += roll(level, maxRolls, allArrays[i])
		sum = sum/100000
		print(f"{allArrays[i]}: {sum}")	
		
		
		
def rerollArrays(min, max, rerolls):
	base = [min]*rerolls
	returnArray = [base.copy()]
	while(base != [max]*rerolls):
		base = increment(base, max, rerolls-1)
		if(sequential(base)):
			returnArray.append(base.copy())
	return returnArray
	
def increment(inList, max, column):
	if(inList[column] == max):
		inList[column] = 0
		return increment(inList, max, column-1)
	inList[column] = inList[column]+1
	return inList

def sequential(inList):
	for i in range(len(inList)-1):
		if(inList[i] > inList[i+1]):
			return False
	return True
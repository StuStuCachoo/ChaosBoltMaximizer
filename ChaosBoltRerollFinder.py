from random import randrange

def roll(level, maxRolls, d8RerollValues, d6RerollValues, armorClass, toHit):
	d1 = randrange(1,9,1)
	d2 = randrange(1,9,1)
	final = 0
	rerolls = maxRolls
	rerollable = []
	for i in range(level):
		curRoll = randrange(1,7,1)
		#while rerolls > 0 and curRoll <d6RerollValues[rerolls-1]:
		#	curRoll = randrange(1,7,1)
		#	rerolls=rerolls-1
		final += curRoll
		if(curRoll < 4):
			rerollable.append([curRoll,6])
	while rerolls > 0 or d1==d2:
		#print(f"{d1},{d2},{rerolls},{final}")
		if(d1 != d2):
			if(d1 > d8RerollValues[rerolls-1] and d2 > d8RerollValues[rerolls-1]):
				break
			elif(d1 < d2):
				d1 = randrange(1,9,1)
			else:
				d2 = randrange(1,9,1)
			rerolls -= 1
		else:
			final += d1 + d2
			if(randrange(1,21,1) + toHit >= armorClass):
				for i in range(0,level):
					curRoll = randrange(1,7,1)
					final += curRoll
					if(curRoll < 4):
						rerollable.append([curRoll,6])
				d1 = randrange(1,9,1)
				d2 = randrange(1,9,1)
			else:
				break
	while rerolls > 0 and len(rerollable) > 0:
		maxUnderAverage = [(rerollable[0][1]+1)/2 - rerollable[0][0],0]
		for i in range(len(rerollable)):
			if (rerollable[i][1]+1)/2 - rerollable[i][0] > maxUnderAverage[0]:
				maxUnderAverage = [(rerollable[i][1]+1)/2 - rerollable[i][0], i]
		diceType = rerollable[maxUnderAverage[1]][1]
		final -= rerollable[maxUnderAverage[1]][0]
		rerollable.pop(maxUnderAverage[1])
		rerolls -= 1
		curRoll = randrange(1,diceType+1,1)
		final += curRoll
		if((curRoll < 4 and diceType == 6) or (curRoll < 5 and diceType == 8)):
			rerollable.append([curRoll,diceType])	
	final += d1 + d2
	return final	
		
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
	
def simRolls(level, maxRolls, armorClass, toHit, numSimulations):
	d8Arrays = rerollArrays(5,8,maxRolls)
	d6Arrays =rerollArrays(1,4,maxRolls)
	for i in range(len(d8Arrays)):
		for j in range(len(d6Arrays)):
			sum = 0
			for k in range(numSimulations):
				sum += roll(level, maxRolls, d8Arrays[i], d6Arrays[j], armorClass, toHit)
			sum = sum/numSimulations
			print(f"{d8Arrays[i]}-{d6Arrays[j]}: {sum}")
			#print(f"{d8Arrays[i]}: {sum}")				
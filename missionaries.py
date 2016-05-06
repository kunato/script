import copy;
import sys;
import math;
sys.setrecursionlimit(10000000)
state = [3,3,1]
OPEN = []
OPEN.append(state)
out = 0
step = 0
log = []
DONE = []
values = []
values.append([])
for i in range(1,100):
	log.append(math.pow(8,i))
while True:
	if(len(OPEN) == 0):
		break
	
	ans = OPEN.pop(0)
	value = values.pop(0)
	DONE.append(ans)
	if(ans[0] == 0 and ans[1] == 0 and ans[2] == 0):
		print (OPEN,ans)
		print value
		price = 0
		for q in value:
			if(q == 0):
				price += 1+(2*0)
			elif(q == 1):
				price += 1+(2*1)
			elif(q == 2):
				price += 1+(2*1)
			elif(q == 3):
				price += 1+(2*2)
			elif(q == 4):
				price += 1+(2*0)
			elif(q == 5):
				price += 1+(2*1)
			elif(q == 6):
				price += 1+(2*3)
			elif(q == 7):
				price += 1+(2*0)
		# break
		print price
	
	if(step in log):
		print math.log(step,8)
	for i in range(0,8):
		value2 = copy.deepcopy(value)
		state_temp = copy.deepcopy(ans)
		if(i == 0):
			action = [0,1,1]
		elif(i == 1):
			action = [1,0,1]
		elif(i == 2):
			action = [1,1,1]
		elif(i == 3):
			action = [2,0,1]
		elif(i == 4):
			action = [0,2,1]
		elif(i == 5):
			action = [1,2,1]
		elif(i == 6):
			action = [3,0,1]
		elif(i == 7):
			action = [0,3,1]
		if(state_temp[2] == 0):
			state_temp[0] += action[0]
			state_temp[1] += action[1]
			state_temp[2] += action[2]
		else:
			state_temp[0] -= action[0]
			state_temp[1] -= action[1]
			state_temp[2] -= action[2]
		value2.append(i)
		if(state_temp[0] > 3 or state_temp[1] > 3 or state_temp[0] < 0 or state_temp[1] < 0):
			continue
		if(state_temp[0] > state_temp[1] and state_temp[1] != 0):
			continue
		if(state_temp[1] > state_temp[0] and state_temp[1] != 3):
			continue
		if(state_temp in DONE):
			continue
		OPEN.append(state_temp)
		values.append(value2)
	# print ("Open",OPEN)
	# print ("Done",DONE)

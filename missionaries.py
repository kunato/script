import copy;
import sys;
import math;
import Queue;
sys.setrecursionlimit(10000000)
state = [3,3,1]
OPEN = Queue.PriorityQueue()
OPEN.put((0,state,[]))
out = 0
step = 0
log = []
DONE = []
for i in range(1,100):
	log.append(math.pow(8,i))
while True:
	if(OPEN.empty()):
		break
	
	ans = OPEN.get()
	DONE.append(ans)
	if(ans[1][0] == 0 and ans[1][1] == 0 and ans[1][2] == 0):
		# print (OPEN,ans)
		price = 0
		value = ans[2]
		# break
		print ("Pass",value,ans[0])
	
	if(step in log):
		print math.log(step,8)
	for i in range(0,8):
		value2 = copy.deepcopy(ans[2])
		state_temp = copy.deepcopy(ans[1])
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
		price = 0;
		if(i == 0):
			price = 1+(2*0)
		elif(i == 1):
			price = 1+(2*1)
		elif(i == 2):
			price = 1+(2*1)
		elif(i == 3):
			price = 1+(2*2)
		elif(i == 4):
			price = 1+(2*0)
		elif(i == 5):
			price = 1+(2*1)
		elif(i == 6):
			price = 1+(2*3)
		elif(i == 7):
			price = 1+(2*0)
		item = (ans[0]+price,state_temp,value2)
		# print ("ITEM",item)
		OPEN.put(item)
	# print ("Open",OPEN)
	# print ("Done",DONE)

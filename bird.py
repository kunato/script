import os
import math3d as m3d
import numpy as np
import random
birds_pos = [];
MATH_PI = 3.14
def generateCode(number):
	bird_number = 400
	#loop add bird
	for i in range(bird_number):
		bird_pos = [random.randrange(-50,50),random.randrange(-50,50),random.randrange(-300,-100),random.uniform(-1.0,1.0),random.randrange(0,1),random.uniform(0.5,1.5),0.0,0.0,[0,0],[0,0]]
		birds_pos.append(bird_pos)
	for i in range(number):
		print "Frame Number :"+str(i)
		f=open('bird/gen'+str(i)+'.pov','w')
		f.write('camera{\nlocation <100,100,100>\nright <1,0,0>\nup <0,1,0>\nangle 30\nlook_at <0,0,0>\n}\nbackground { color rgb <0.5, 0.9, 1.0> }\nlight_source{<100,100,1000> color <1, 1, 1>}\n')
		###mesh{
		##loop bird number
		for i in range(len(birds_pos)):
			pos = birds_pos[i]
			data = pos[:3]
			counter = pos[3]
			plus = pos[4]
			rot = pos[6:8]
			#wingstep -1 < x < 1
			if(plus == 1):
				counter+=0.05
			else:
				counter-=0.05
			offset =pos[8]
			sign = pos[9]
	 		data,rot,offset,sign = genBird(f,data,counter,pos[5],rot,i,offset,sign);
	 		# data[0]+=1
	 		# data[1]+=1
	 		pos[5]+=random.uniform(-0.05,0.05)
	 		if(pos[5] <= 1.0):
	 			pos[5] = 1.0
			if(counter >= 1.0):
				plus = -1
			if(counter <= -1.0):
				plus = 1
			pos[3] = counter
			pos[4] = plus
			pos[:3] = data
			pos[6:8] = rot
			pos[8] = offset
			pos[9] = sign
			# print (offset,sign)

def genBird(f,pos,wingstep,speed,rot,number,offset,sign):
	body = [m3d.Vector(0,-1,-5),m3d.Vector(0,2,-5),m3d.Vector(0,1,6)]
	l_wing = [m3d.Vector(0,1,-3),m3d.Vector(-4,6*wingstep,0),m3d.Vector(0,1,3)]
	r_wing = [m3d.Vector(0,1,3),m3d.Vector(4,6*wingstep,0),m3d.Vector(0,1,-3)]
	offset1 = offset[0]
	offset2 = offset[1]
	sign_sigma = sign[0]
	sign_delta = sign[1]
	turn = random.randrange(0,100)
	if(turn < 10 or turn < offset1):
		if(offset1 == 0):
			sign_sigma = random.randint(0, 1)
			offset1 = 95
		else:
			offset1-=3
		if(sign_sigma == 0):
			sigma = random.uniform(0.0,1.0)*MATH_PI/60
		else:
			sigma = -1.0 * random.uniform(0.0,1.0)*MATH_PI/60
	else:
		sigma = 0.0
		offset1 = 0
		# sigma = random.uniform(-1.0,1.0)*MATH_PI/5
	if(turn > 10 or turn < offset2):
		if(offset2 == 0):
			sign_delta = random.randint(0, 1)
			offset2 = 95
		else:
			offset2-=3
		if(sign_delta == 0):
			delta = random.uniform(0.0,1.0)*MATH_PI/60
		else:
			delta = -1.0 * random.uniform(0.0,1.0)*MATH_PI/60
		
	else:
		delta = 0.0
		offset2 = 0
		# delta = random.uniform(-1.0,1.0)*MATH_PI/5
	rot[0]+=sigma
	roty = m3d.Orientation.new_axis_angle([0,3,0],rot[0])
	
	rot[1]+=delta
	rotx = m3d.Orientation.new_axis_angle([-3,0,0],rot[1])
	rotxy = roty*rotx
	# print('rots',number,rotx,roty)
	for i in range(3):

		body[i] = rotxy * body[i]
		l_wing[i] = rotxy * l_wing[i]
		r_wing[i] = rotxy * r_wing[i]
	pos[0]= pos[0]+ speed*(np.sin(rot[0]))
	pos[1]= pos[1]+ speed*(np.sin(rot[1]))
	pos[2]= pos[2]+ speed*((np.cos(rot[0]) * np.cos(rot[1])))
	# print ('pos',pos)
	# print ('rot',number,(rot[0]*180/MATH_PI),(rot[1]*180/MATH_PI))
	# print wingstep
	#change -+4
	body[0][:]+=pos[:]
	body[1][:]+=pos[:]
	body[2][:]+=pos[:]
	l_wing[0][:]+=pos[:]
	l_wing[1][:]+=pos[:]
	l_wing[2][:]+=pos[:]
	r_wing[0][:]+=pos[:]
	r_wing[1][:]+=pos[:]
	r_wing[2][:]+=pos[:]
	# print (body,l_wing,r_wing)
	f.write('object{\nmesh{\n');
	f.write('triangle {<%d,%d,%d>, <%d,%d,%d>, <%d,%d,%d>}'%(body[0][0],body[0][1],body[0][2],body[1][0],body[1][1],body[1][2],body[2][0],body[2][1],body[2][2]));
	f.write('pigment{ color <0.9, 0.9, 0.9>}\nfinish { diffuse 1.0 ambient 1.0 }\n}}');
	f.write('object{\nmesh{\n');
	f.write('triangle {<%d,%d,%d>, <%d,%d,%d>, <%d,%d,%d>}'%(l_wing[0][0],l_wing[0][1],l_wing[0][2],l_wing[1][0],l_wing[1][1],l_wing[1][2],l_wing[2][0],l_wing[2][1],l_wing[2][2]));
	f.write('triangle {<%d,%d,%d>, <%d,%d,%d>, <%d,%d,%d>}'%(r_wing[0][0],r_wing[0][1],r_wing[0][2],r_wing[1][0],r_wing[1][1],r_wing[1][2],r_wing[2][0],r_wing[2][1],r_wing[2][2]));
	f.write('pigment{ color <1, 1, 1>}\nfinish { diffuse 1.0 ambient 0.9 }\n}}');
	offset = [offset1,offset2]
	sign = [sign_sigma,sign_delta]
	return (pos,rot,offset,sign)
size = 600
generateCode(size);
for i in range(size):
	os.system('./povray/Povray37UnofficialMacCmd bird/gen'+str(i)+'.pov sphere.ini')
	print "Running : "+str(i/float(size)*100)+"%"
	# os.system('osascript ~/preview.scpt')
os.system('ffmpeg -r 50 -i bird/gen%d.png  -vcodec mpeg4 -b 4M -crf 10  bird.mp4')

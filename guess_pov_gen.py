import math
import os 

def gauss(x,y,gramma):
	s2 = gramma*gramma
	return 1.0 / math.sqrt(2.0*3.1416*s2) *  math.exp(-(x*x + y*y) / (2.0*s2))

	
def generateCode(range1,range2,gramma,name):
	l = 100
	f=open('data/gen'+str(name)+'.pov','w')
	f.write('camera{\nlocation <0, -5, 5>\nright <-1.33, 0, 0>\nup <0, 0, 1>\nangle 30\nlook_at  <0, 0, 0>\n}\nlight_source{ <5, -5, 5> color rgb <1, 1, 1> }\nobject{\nmesh{\n')
	array = [[0 for i in range(l)] for j in range(l)]
	w = 1.0/l * (range2-range1)
	for i in range(0,l):
		for j in range(0,l):
			# print range1
			# print (range1 + (i * w) , range1 +(j * w))
			x = range1 + (i * w) 
			y = range1 + (j * w)
			z = gauss(x,y,gramma)
			array[i][j] = (x,y,z)

	for i in range(0,l-1):
		for j in range(0,l-1):
			p0 = array[i][j]
			p1 = array[i+1][j]
			p2 = array[i][j+1]
			p3 = array[i+1][j+1]
			triangle1 = "triangle {<%s,%s,%s>, <%s,%s,%s>, <%s,%s,%s>}\n"%(p0[0],p0[1],p0[2],p1[0],p1[1],p1[2],p3[0],p3[1],p3[2])
			f.write(str(triangle1))

			triangle2 = "triangle {<%s,%s,%s>, <%s,%s,%s>, <%s,%s,%s>}\n"%(p0[0],p0[1],p0[2],p3[0],p3[1],p3[2],p2[0],p2[1],p2[2])
			
			f.write(str(triangle2))
			

			# print triangle1
			# print triangle2
	f.write("}\npigment{ color <0, 1, 0> }\nfinish{ diffuse 1.0 ambient 0.0 }\n}")



#DGaussFunction(0,0,1)
total_calc = 150
for i in range(1,total_calc):
	start = 0.1
	now = start + ((float(i)/total_calc)*1.5);
	print "gramma : "+str(now)
	generateCode(-5,5,now,i)
	os.system('./povray/Povray37UnofficialMacCmd data/gen'+str(i)+'.pov sphere.ini')
	print "Running : "+str(i/float(total_calc)*100)+"%"


	
import numpy as np
import math
import matplotlib.pyplot as plt
s = 100
p = 0.3
array = []
array2 = []
for i in range(0,100):
	p = float(i)/float(s)
	p3 = p*p*p
	p2 = (1-p)*p*p
	p1 = (1-p)*(1-p)*p
	p0 = (1-p)*(1-p)*(1-p)
	sums = 0
	sums+=2*p0#BBB
	sums+=2*p1#BBA
	sums+=3*p1#BAB
	sums+=4*p2#BAA
	sums+=3*p1#ABB
	sums+=4*p2#ABA
	sums+=4*p2#AAB
	sums+=4*p3
	array.append(sums)
	array2.append(p)
	print sums
print array
plt.plot(array2,array)
plt.xlabel('Probability p')
plt.ylabel('Average Codeword Length')
# plt.axis([2, 4, 0, 100])
plt.show()
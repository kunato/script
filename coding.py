import math
from decimal import *
f = math.factorial
a = 0.3
b = 0.7
n = 100
ssum = 0
ssum2 = Decimal(0)
for i in range(65,76):
	ans = f(n)/(f(i)*f(n-i))
	ssum += ans
	ssum2 += (Decimal(ans)) * Decimal(a ** i) * Decimal(b**(n-i)) 
	print ans, Decimal(ans) * Decimal(a ** i) * Decimal(b**(n-i)) ,Decimal(a ** i) * Decimal(b**(n-i))
print ssum
print "ANS"
print 2**n
print Decimal(ssum)/Decimal(2**n)
print ssum2
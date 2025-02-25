import numpy as np
import math

x = [-0.33041522, -0.04623482, 0.94270265]
y = [-0.33040872, -0.04607474, 0.94271266]
#print(y[1])
xpn = x[0]*y[0] + x[1]*y[1]+ x[2]*y[2]
a1 = math.sqrt(pow(x[0],2) + pow(x[1],2) + pow(x[2],2))
a2 = math.sqrt(pow(y[0],2) + pow(y[1],2) + pow(y[2],2))
cosp = xpn / (a1*a2)
print(cosp)

print(np.dot(x,y))


print(a1)
print(np.linalg.norm(x))
print(a2)
print(np.linalg.norm(y))
print(a1*a2)
print(np.linalg.norm(x)*np.linalg.norm(y))
# x2 = np.array(x)
# temp = math.sqrt(pow(x2[0],2) + pow(x2[1],2) + pow(x2[2],2))
# print(a1)
# print(temp)
__author__ = 'Kevin'
from calculateSlope import calculateSlope
import random
A=[]
for i in range(60):
    A.append(random.randint(-1,1))
print A
print calculateSlope(A)

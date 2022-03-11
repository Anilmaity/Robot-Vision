# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:23:32 2020

@author: DELL
"""

T = input()
L = input()

L = L.split(" ")
for x in range(len(L)):
    L[x] = int(L[x])
    
a = L[0]
d = L[1]
n = L[2]
AP =[]
SumofAP =0
for x in range(n):
      AP.append(a+d*x)
      SumofAP = SumofAP + a+d*x
print(AP) 
print(SumofAP)   
      
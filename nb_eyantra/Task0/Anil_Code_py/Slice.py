# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 18:49:47 2020

@author: DELL
"""

T = int(input())
for x in range(T):
    Size = int(input())
    L = input()
    List =  L.split(" ")

    for x in range(Size):
            List[x] = int(List[x]) 
    s = List[::-1]
    
    print(s) 
    Temp = List[0::3]
    for m in range(len(Temp)):
        Temp[m]=Temp[m]+3
        
    print(Temp)    
    Temp = List[0::5]
    for m in range(len(Temp)):
        Temp[m]=Temp[m]-7
    print(Temp)
    Sum = 0  
    for x in range(3,8):
        Sum = Sum + List[x]
    print(Sum)    
    

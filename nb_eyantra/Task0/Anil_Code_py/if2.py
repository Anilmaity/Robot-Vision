# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 17:12:40 2020

@author: DELL
"""

T = int(input("Enter T"))
r = []

for a in range(T):
    r.append(int(input()))

for i in range(0,T):
    for b in range(r[i]):
       print(b, end =" ")   
    print("")   
       
       
    
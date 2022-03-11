# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 17:40:47 2020

@author: DELL
"""
import math as m

TC = int(input())
C = []
Distance = []
for a in range(TC):
    I = input()

    C.append(I.split(' '))
    for x in range(4):
        C[a][x] = float(C[a][x])
    print(C)
    Distance.append(float(m.sqrt(pow(C[a][0] - C[a][2], 2) +
                                 pow(C[a][1] - C[a][3], 2))))

for d in range(TC):
    print("Distance = " + str("{0:.2f}".format(Distance[d])))

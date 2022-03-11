# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
n = int(input("Insert an integer number"))
i = 0
for i in range(n) :
    
    if i != 0:
        if i%2 == 0:
            print(i*i)
        else:
            print(2*i)
    else:
        print(i+3)
    i= i+1


    
        
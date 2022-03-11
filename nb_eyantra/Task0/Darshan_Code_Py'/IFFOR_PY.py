'''
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code IFFOR_PY
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:            IFFOR_PY.py
*  Created:             19/09/2020
*  Last Modified:       21/09/2020
*  Author:              e-Yantra Team
*
*****************************************************************************************
'''
import sys
def inputs():# for input
    for line in sys.stdin:
        line.rstrip()
        break
    return line #returning input value
# Main function
if __name__ == '__main__':
    
    # Take the T (test_cases) input
    test_cases = int(inputs()) # calling input function
    # Write your code from here
    i=0
    if test_cases >= 1 and test_cases <=25: # taking test cases values from 1 to 25
        for i in range(0, test_cases):
            test_case = int(inputs())
            if test_case >= 0 and test_case<=100: # taking test cases values from 0 to 100
                test_case_list=[]
                for j in range(0,test_case):
                    if j == 0: # if value is 0 it will replace it by 3
                        test_case_list.append(3)
                    elif j%2 == 0: # if value is even it will replace it by it's double
                        test_case_list.append(j*2)
                    elif j%2 == 1: # if value is odd it will replace it by it's square
                        test_case_list.append(j*j)
                for result in test_case_list:
                    print(" ", result, end =" ")
                print("\n")        
    








        



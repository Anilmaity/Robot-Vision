'''
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code SLICE_PY
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:            SLICE_PY.py
*  Created:             04/10/2020
*  Last Modified:       04/10/2020
*  Author:              e-Yantra Team
*
*****************************************************************************************
'''
def check_int(s):# function for checking integer 
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()
# Main function
if __name__ == '__main__':
    
    # Take the T (test_cases) input
    test_cases = int(input())
    
    flag = True
    # Write your code from here
    if test_cases >=0 and test_cases <= 25: #checking constraints on number of test cases
        for k in range(0, test_cases):
            size = int(input())
            if size<8 and size>50: # checking constraint on length
                print(" constraint on length is not followed ")
                flag = False
                break
            input_array = list(input().split(" "))
            for j in range(0,size):
                if not check_int(input_array[j]): #checking constraint on input value type
                    print("constraint on array values is not followed")
                    flag = False
                    break
                if int(input_array[j])< -100 and int(input_array[j])>100: # checking constraint on input values range
                    print("constraint on array values is not followed")
                    flag = False
                    break

            if flag == True:
                new_lst = input_array[::-1] # reversing the array
                # for i in range(0,size)
                for j in range(0,size): #printing the reverse array
                    print(new_lst[j], end=" ")
                print("\n")
                for j in range(0, size): # printing the third number
                    if j != 0:
                        if (j)%3 == 0:
                            third_number = int(input_array[j])+3
                            print(third_number, end=" ")
                print("\n")            
                for j in range(0, size): # printing the fifth number
                    if j != 0:
                        if (j)%5 == 0:
                            fifth_number = int(input_array[j])-7
                            print(fifth_number, end=" ")
                print("\n")            
                total = 0
                for j in range(0, size): # printing the total of 3 to 7 values
                    if j>2 and j<8:
                        total = total + int(input_array[j])
                print(total)
            else:
                break




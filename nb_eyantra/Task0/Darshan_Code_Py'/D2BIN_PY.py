'''
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code D2BIN_PY
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:			D2BIN_PY.py
*  Created:				04/10/2020
*  Last Modified:		04/10/2020
*  Author:				e-Yantra Team
*
*****************************************************************************************
'''


# function to calculate raw binary number using recursion
def dec_to_binary_recursion(k):
    if k > 1:
        a = dec_to_binary_recursion(k//2)+str(k % 2)
        return a
    else:
        return str(k % 2)


def dec_to_binary(n):
    bin_num = None
    # Complete this function to return binary equivalent output of the given number 'n' in 8-bit format

    temp_str = ""
    # calling function to return raw binary data
    binary_value = dec_to_binary_recursion(n)
    size = len(binary_value)
    for i in range(0, 8):  # loop for adding remaining zeros
        if i < (8-size):
            temp_str = temp_str + "0"
    temp_str = temp_str + str(binary_value)  # adding zeros to the binary value

    bin_num = temp_str

    return bin_num


# Main function
if __name__ == '__main__':

    # take the T (test_cases) input
    test_cases = int(input())

    # Write the code here to take the n value
    for case in range(1, test_cases+1):
        # take the n input values
        n = int(input())

        # print (n)

        # Once you have the n value, call the dec_to_binary function to find the binary equivalent of 'n' in 8-bit format
        bin_num = dec_to_binary(n)
        print(bin_num)

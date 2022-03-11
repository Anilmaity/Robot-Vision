"""
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code APLAM_PY
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:			APLAM_PY.py
*  Created:				04/10/2020
*  Last Modified:		04/10/2020
*  Author:				e-Yantra Team
*
*****************************************************************************************
"""

# Import reduce module
from functools import reduce


# Function to calculate Euclidean distance between two points

def generate_AP(a1, d, n):
    # Complete this function to return A.P. series
    AP_series = []

    for j in range(0, n):
        nth_number = a1 + j*d
        AP_series.append(nth_number)

    return AP_series


# Main function
if __name__ == '__main__':

    # take the T (test_cases) input
    test_cases = int(input())

    # Write the code here to take the a1, d and n values
    if 1 <= test_cases <= 25:  # checking constraint for test case
        for i in range(0, test_cases):
            user_input = list(input().split(" "))
            a1 = int(user_input[0])
            d = int(user_input[1])
            n = int(user_input[2])
            # checking the constraints for arguments
            if (1 <= a1 <= 100) and (1 <= d <= 100) and (1 <= n <= 100):

                # Once you have all 3 values, call the generate_AP function to find A.P. series and print it
                # calling generate_AP function
                AP_series = generate_AP(a1, d, n)
                for k in AP_series:
                    print(k, end=" ")
                print("\n")
                # Using lambda and map functions, find squares of terms in AP series and print it
                # squaring the series
                sqr_AP_series = list(map(lambda x: x*x, AP_series))
                for k in sqr_AP_series:
                    print(k, end=" ")
                print("\n")

                # Using lambda and reduce functions, find sum of squares of terms in AP series and print it
                # summing the squared series
                sum_sqr_AP_series = reduce(lambda a, b: a+b, sqr_AP_series)
                print(sum_sqr_AP_series)
            else:
                print("test case constraint not followed")



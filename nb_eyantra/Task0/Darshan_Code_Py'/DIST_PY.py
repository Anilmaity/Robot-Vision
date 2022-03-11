"""
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code DIST_PY
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:            DIST_PY.py
*  Created:             02/10/2020
*  Last Modified:       02/10/2020
*  Author:              e-Yantra Team
*
*****************************************************************************************
"""

# Import any required module/s
import math

# Function to calculate Euclidean distance between two points
def compute_distance( x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))  # applying the euclidean distance method
    print("Distance = " + str("{0:.2f}".format(distance)))
    # Complete this function to return Euclidean distance and
    # print the distance value with precision up to 2 decimal places


# Main function
if __name__ == '__main__':

    # Take the T (test_cases) input
    test_cases = int(input())

    # Write the code here to take the x1, y1, x2 and y2 values
    # checking constraints on test cases are not violated
    if 1 <= test_cases <= 25:
        for i in range(0, test_cases):
            coordinates = list(input().split(" "))
            # converts the input into list
            x1 = float(coordinates[0])
            y1 = float(coordinates[1])
            x2 = float(coordinates[2])
            y2 = float(coordinates[3])
            # checking whether the constraints on coordinates are not violated
            if -100 <= x1 <= 100 and -100 <= x2 <= 100 and -100 <= y1 <= 100 and -100 <= y2 <= 100:
                compute_distance(x1, y1, x2, y2)
            else:
                print("coordinates are not proper")
            # calling the function
    else:
        print("value of test case is not proper")

        # print(x1,y1,x2,y2)

    # Once you have all 4 values, call the compute_distance function to find Euclidean distance

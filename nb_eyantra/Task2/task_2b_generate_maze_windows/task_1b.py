'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv


##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


##############################################################


def applyPerspectiveTransform(input_img):
    """
    Purpose:
    ---
    takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

    Input Arguments:
    ---
    `input_img` :   [ numpy array ]
        maze image in the form of a numpy array

    Returns:
    ---
    `warped_img` :  [ numpy array ]
        resultant warped maze image after applying Perspective Transform

    Example call:
    ---
    warped_img = applyPerspectiveTransform(input_img)
    """

    warped_img = None

    ##############	ADD YOUR CODE HERE	##############

    gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)  # Converting the image to gray scale
    temp, binary_image = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY)  # Converting the image into binary image pixil will be either 0 or 255
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Finding the contours
    contour_img = cv2.drawContours(gray_img, contours, -1, (0, 0, 0), 2)

    #############################################################
    # In this section finding the 4 end points of the maze their in the contours

    '''         x1,y1________x2,y2
                    |        |
              x3,y3 |________| x4,y4
    '''

    n = contours[1].ravel()  # n contain all the point of outer contour  detected
    max = n[0] + n[1]  # n[even numbers] is value of row and n[odd number] is column of the maze
    min = n[0] + n[1]
    max2 = 0
    max3 = 0

    # basically the n[x] hold the location of pixil where their a point (point which lies on the outer lines in maze)
    # so x1,y1 which we want will ne in n[] and has the minimum value
    # From this logic all 4 point can be available

    x1, y1, x2, y2, x3, y3, x4, y4 = 0,0,0,0,0,0,0,0
    for x in range(len(n)):
        if x % 2 == 0:
            if n[x + 1] + n[x] > max:
                max = n[x + 1] + n[x]
                x4 = n[x]
                y4 = n[x + 1]
            if n[x + 1] + n[x] < min:
                min = n[x + 1] + n[x]
                x1 = n[x]
                y1 = n[x + 1]
            if n[x] > 256:
                if n[x] - n[x + 1] > max2:
                    max2 = n[x] - n[x + 1]
                    x2 = n[x]
                    y2 = n[x + 1]
            if n[x + 1] > 256:
                if n[x + 1] - n[x] > max3:
                    max3 = n[x + 1] - n[x]
                    x3 = n[x]
                    y3 = n[x + 1]


    # ____________________________________________________________

    pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])   # end ponits of maze
    pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]]) # end point of image which is 500*500
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped_img = cv2.warpPerspective(contour_img, M, (500, 500))  # warping image

    # some times the end points are not aligned with the image so manually assign black colour to the border
    warped_img[0::, 0:2] = 0
    warped_img[0:2, 0::] = 0
    warped_img[0::, 498:500] = 0
    warped_img[498:500, 0::] = 0

    #cv2.imshow('warped img', warped_img)
    #cv2.waitKey()

    ##################################################

    return warped_img


def detectMaze(warped_img):
    """
    Purpose:
    ---
    takes the warped maze image as input and returns the maze encoded in form of a 2D array

    Input Arguments:
    ---
    `warped_img` :    [ numpy array ]
        resultant warped maze image after applying Perspective Transform

    Returns:
    ---
    `maze_array` :    [ nested list of lists ]
        encoded maze in the form of a 2D array

    Example call:
    ---
    maze_array = detectMaze(warped_img)
    """

    maze_array = []

    ##############	ADD YOUR CODE HERE	##############
    temp, binary_image = cv2.threshold(warped_img, 80, 255, cv2.THRESH_BINARY)  # converting image to binary

    cellMatrix = []  # it will contain all the values of maze

    for k in range(0, 10):
        for l in range(0, 10):
            cellimage = binary_image[(k * 50):(k * 50) + 50, (l * 50):(l * 50) + 50]  # their will be 100 small images  each 50*50 represent the cell image

            # W_side holds the value of all 1st column which is west side of the image
            # CellImage side decide the value assign to it

            W_side = cellimage[0::, 0]
            N_side = cellimage[0, 0::]
            E_side = cellimage[0::, 49]
            S_side = cellimage[49, 0::]

            w_avg = 0
            n_avg = 0
            s_avg = 0
            e_avg = 0

            for i in range(50):  # suming all values of all side
                w_avg += W_side[i]
                n_avg += N_side[i]
                s_avg += S_side[i]
                e_avg += E_side[i]

            w_avg /= 50
            n_avg /= 50
            s_avg /= 50
            e_avg /= 50

            cell_sum = 0  # initilize the cell_sum as 0 for each loop
            if w_avg < 0.5 * 255:
                cell_sum += 1
            if n_avg < 0.5 * 255:
                cell_sum += 2
            if e_avg < 0.5 * 255:
                cell_sum += 4
            if s_avg < 0.5 * 255:
                cell_sum += 8
            cellMatrix.append(cell_sum)  # storing the cell_sum in cellmatrix

    maze_array = np.array(cellMatrix)
    maze_array = maze_array.reshape(10, 10)
    maze_array = maze_array.tolist()

    ##################################################

    return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):
    """
    Purpose:
    ---
    takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

    Input Arguments:
    ---
    `csv_file_path` :	[ str ]
        file path with name for csv file to write

    `maze_array` :		[ nested list of lists ]
        encoded maze in the form of a 2D array

    Example call:
    ---
    warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
    """

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

    # path directory of images in 'test_cases' folder
    img_dir_path = 'test_cases/'

    # path to 'maze00.jpg' image file
    file_num = 6
    img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

    print('\n============================================')
    print('\nFor maze0' + str(file_num) + '.jpg')

    # path for 'maze00.csv' output file
    csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

    # read the 'maze00.jpg' image file
    input_img = cv2.imread(img_file_path)

    # get the resultant warped maze image after applying Perspective Transform
    warped_img = applyPerspectiveTransform(input_img)

    if type(warped_img) is np.ndarray:

        # get the encoded maze in the form of a 2D array
        maze_array = detectMaze(warped_img)

        if (type(maze_array) is list) and (len(maze_array) == 10):

            print('\nEncoded Maze Array = %s' % (maze_array))
            print('\n============================================')

            # writes the encoded maze array to the csv file
            writeToCsv(csv_file_path, maze_array)

            cv2.imshow('warped_img_0' + str(file_num), warped_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:

            print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
            exit()

    else:

        print(
            '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
        exit()

    choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 9):

            # path to image file
            img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

            print('\n============================================')
            print('\nFor maze0' + str(file_num) + '.jpg')

            # path for csv output file
            csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

            # read the image file
            input_img = cv2.imread(img_file_path)

            # get the resultant warped maze image after applying Perspective Transform
            warped_img = applyPerspectiveTransform(input_img)

            if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                    print('\nEncoded Maze Array = %s' % (maze_array))
                    print('\n============================================')

                    # writes the encoded maze array to the csv file
                    writeToCsv(csv_file_path, maze_array)

                    cv2.imshow('warped_img_0' + str(file_num), warped_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                else:

                    print(
                        '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:

                print(
                    '\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:

        print('')

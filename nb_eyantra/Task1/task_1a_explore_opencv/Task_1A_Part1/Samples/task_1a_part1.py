'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Filename:			task_1a_part1.py
# Functions:		scan_image
# 					[ Comma separated list of functions in this file ]
# Global variables:	shapes
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


##############################################################


def scan_image(img_file_path):
    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }

    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes

    ##############	ADD YOUR CODE HERE	##############

    img = cv2.imread(img_file_path)  # reading image
    # reading image in grayscale
    img_count = cv2.imread(img_file_path, cv2.IMREAD_GRAYSCALE)

    shape_dict = {}

    # thresholding the greyscale image
    _, threshold = cv2.threshold(img_count, 240, 255, cv2.THRESH_BINARY)
    contours, image = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contouring all shapes in image
    # print("contours", len(contours))
    for i in range(1, 4):
        # converting original image to hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # print(len(contours))
        if i == 1:  # loop 1 to detect red shapes
            lower_range = np.array([0, 50, 50])
            upper_range = np.array([10, 255, 255])
        elif i == 2:  # loop 1 to detect blue shapes
            lower_range = np.array([94, 80, 2])
            upper_range = np.array([126, 255, 255])
        elif i == 3:  # loop 1 to detect green shapes
            lower_range = np.array([25, 52, 72])
            upper_range = np.array([102, 255, 255])

        # selecting shapes with colour based on loops
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # thresholding the original image
        _, threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
        contours, image = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contouring the selected shapes

        for cnt in contours:  # loop for all selected shapes
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            cv2.drawContours(img, [approx], 0, (0), 5)  # drawing contours
            area = cv2.contourArea(cnt)  # determining area
            M = cv2.moments(cnt)
            # determing centroid X coordinate
            cX = int(M["m10"] / float(M["m00"]))
            cY = int(M["m01"] / M["m00"])  # determing centroid y coordinate
            # print(area)
            # print(cX)
            # print(cY)

            # appending the required information for the shape
            temp_list = []
            if i == 1:
                temp_list.append("red")
            elif i == 2:
                temp_list.append("blue")
            elif i == 3:
                temp_list.append("green")
            temp_list.append(area)
            temp_list.append(cX)
            temp_list.append(cY)

            if len(approx) == 4:  # for shape with 4 sides
                x, y, w, h = cv2.boundingRect(cnt)
                # print(x,y)
                # print(w, h)
                # aspect_ratio = int(int(w)/int(h))
                # print("aspect ratio", aspect_ratio)

                # determining coordinates (a, b)
                a1 = approx[0][0][0]
                b1 = approx[0][0][1]
                a2 = approx[1][0][0]
                b2 = approx[1][0][1]
                a3 = approx[2][0][0]
                b3 = approx[2][0][1]
                a4 = approx[3][0][0]
                b4 = approx[3][0][1]

                l1 = ((a2-a1)*(a2-a1) + (b2-b1)*(b2-b1))**0.5  # length 1
                # print("length of line1: ", int(l1))
                l2 = ((a3-a2)*(a3-a2) + (b3-b2)*(b3-b2))**0.5  # length 2
                # print("length of line2: ", int(l2))
                l3 = ((a4-a3)*(a4-a3) + (b4-b3)*(b4-b3))**0.5  # length 3
                # print("length of line3: ", int(l3))
                l4 = ((a4-a1)*(a4-a1) + (b4-b1)*(b4-b1))**0.5  # length 3
                # print("length of line4: ", int(l4))
                # print(a1, b1, a2, b2, a3, b3, a4, b4)

                # checking for square or parallelogram
                if int(l1) <= int(l2)+2 and int(l1) >= int(l2)-2 and int(l1) <= int(l3)+2 and int(l1) >= int(l3)-2 and int(l1) <= int(l4)+2 and int(l1) >= int(l4)-2:

                    if int(l1) <= h+5 and int(l1) >= h-5:
                        shape_dict['Square'] = temp_list
                    else:
                        shape_dict['Parallelogram'] = temp_list
                # checking for rectangle or parallelogram
                elif int(l1) == int(l3) and int(l2) == int(l4):
                    if int(l1) <= h+5 and int(l1) >= h-5:
                        shape_dict['Rectangle'] = temp_list
                    else:
                        shape_dict['Parallelogram'] = temp_list
                # checkng for trapezium
                elif int(l4) < int(l2):
                    shape_dict['Trapezium'] = temp_list

                # print(approx)
            # checking for circle
            elif len(approx) == 16:
                shape_dict['Circle'] = temp_list
                # print("circle")
            # checking for triangle
            elif len(approx) == 3:
                # print("triangle")
                shape_dict['Triangle'] = temp_list
            # checking for pentagon
            elif len(approx) == 5:
                # print("pentagon")
                shape_dict['Pentagon'] = temp_list
            # checking for hexagon
            elif len(approx) == 6:
                # print("pentagon")
                shape_dict['Hexagon'] = temp_list
            # print(shape_dict)
    #     # M = cv2.moments(cnt)
    #     # print( M )
    #     # print(len(approx))
    shapes = shape_dict

    # cv2.imshow("shapes", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ##################################################

    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in ' + curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'

    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')

    else:
        print('\n[ERROR] Sample' + str(file_num) +
              '.png not found. Make sure "Samples" folder has the selected file.')
        exit()

    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' +
              img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')

        else:
            print('\n[ERROR] scan_image function returned a ' +
                  str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print(
            '\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input(
        '\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2

        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + \
                'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')

            else:
                print('\n[ERROR] Sample' + str(file_num + 1) +
                      '.png not found. Make sure "Samples" folder has the selected file.')
                exit()

            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' +
                      img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')

                else:
                    print('\n[ERROR] scan_image function returned a ' +
                          str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print(
                    '\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')

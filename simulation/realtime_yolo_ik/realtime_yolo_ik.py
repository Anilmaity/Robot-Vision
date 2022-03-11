import pandas as pdq
import yolov5
import time

import numpy as np
import cv2
import os
import sys
import traceback
import pandas as pd
import math
from inverse_kinematics import inverse_kinematics

##############################################################

pre_time = 0
crt_time = 0

try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print(
        'sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
    sys.exit()

client_id = -1


def init_remote_api_server():
    global client_id

    ##############	ADD YOUR CODE HERE	##############

    sim.simxFinish(-1)  # just in case, close all opened connections
    client_id = sim.simxStart("127.0.0.1", 19997, True,
                              True, 5000, 5)  # start aconnection

    ##################################################

    return client_id


def start_simulation():
    global client_id

    return_code = 0

    return_code = sim.simxStartSimulation(
        client_id, sim.simx_opmode_oneshot_wait)

    return return_code


def transform_vision_sensor_image(vision_sensor_image, image_resolution, scaling):
    transformed_image = None

    ##############	ADD YOUR CODE HERE	##############
    # print(vision_sensor_image)
    transformed_image = np.array(vision_sensor_image, dtype=np.uint8)

    transformed_image.resize([image_resolution[0], (image_resolution[1]), 3])

    stretch_near = cv2.resize(transformed_image, (scaling * image_resolution[1], (image_resolution[1]) * scaling),
                              interpolation=cv2.INTER_NEAREST)

    stretch_near = cv2.cvtColor(stretch_near, cv2.COLOR_BGR2RGB)
    stretch_near = cv2.flip(stretch_near, 0)

    ##################################################

    return stretch_near


def stop_simulation():
    global client_id

    return_code = 0

    ##############	ADD YOUR CODE HERE	##############

    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)

    ##################################################

    return return_code


def exit_remote_api_server():
    global client_id

    ##############	ADD YOUR CODE HERE	##############

    sim.simxFinish(-1)



def scan_image(img):


    global shapes

    ##############	ADD YOUR CODE HERE	##############

    # img = cv2.imread(img_file_path)  # reading image
    # reading image in grayscale
    img_count = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)

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
    shapes = shape_dict
    print(shapes)



    ##################################################

    return shapes


def move_joint(jointhandler, position, gripper):
    for i, obj in enumerate(jointhandler):
        # print(i, obj)
        code = sim.simxSetJointTargetPosition(
            client_id, obj, position[i] * math.pi / 180, sim.simx_opmode_oneshot_wait)
    # print(code)

    if (gripper == 'close'):
        sim.simxClearIntegerSignal(
            client_id, 'NiryoLGripper_close', sim.simx_opmode_oneshot_wait)
    else:
        sim.simxSetIntegerSignal(
            client_id, 'NiryoLGripper_close', 1, sim.simx_opmode_oneshot_wait)


def control_joints(joint, degree):
    print('redundantRob_joint' + str(1 + joint))
    code, joint = sim.simxGetObjectHandle(client_id, 'redundantRob_joint' + str(1 + joint),
                                          sim.simx_opmode_oneshot_wait)
    print(code)
    code = sim.simxSetJointTargetPosition(
        client_id, joint, degree * 3.14 / 180, sim.simx_opmode_oneshot_wait)
    print(code)

    # for i in range(degree):
    #     code = sim.simxSetJointTargetPosition(client_id, joint, i,sim.simx_opmode_oneshot)
    #     print(code)
    #     code = sim.simxSetJointPosition(client_id, joint, i,sim.simx_opmode_oneshot)
    #     print(code)
    #

    return code


if __name__ == "__main__":
    pickpos = False

    client_id = init_remote_api_server()
    print(client_id)

    model = yolov5.load('yolov5s.pt')

    time.sleep(1)
    JointHandler = []
    for i in range(6):
        print('NiryoOneJoint' + str(i + 1))
        code, handler = sim.simxGetObjectHandle(
            client_id, 'NiryoOneJoint' + str(i + 1), sim.simx_opmode_oneshot_wait)
        JointHandler.append(handler)

    code, visionSensorHandle = sim.simxGetObjectHandle(
        client_id, 'Vision', sim.simx_opmode_oneshot_wait)

    print(code)

    return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0,
                                                                                      sim.simx_opmode_streaming + 25)

    return_code = start_simulation()

    print(return_code)

    start_time = 0

    object_pick_list = ['sports ball']
    while True:
        crt_time = time.time()
        tt = int((crt_time - pre_time) * 1000)
        pre_time = crt_time
        fps = int((1 / tt) * 1000)
        '''
        joint = int(input("joint (0-6) : "))

        if joint <= 7:
            degree = int(input("degree : "))
            move_joint([JointHandler[joint]], [degree], 'open')
        else:
            break
        '''
        return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle,
                                                                                          0,
                                                                                          sim.simx_opmode_oneshot_wait)

        img = transform_vision_sensor_image(
            vision_sensor_image, image_resolution, 1)



        cv2.imshow('transformed image', img)

        q = cv2.waitKey(1)
        if q == ord("q"):
            break

    cv2.destroyAllWindows()

    return_code = stop_simulation()

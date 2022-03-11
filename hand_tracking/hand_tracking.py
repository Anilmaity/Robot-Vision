import cv2 as cv
import mediapipe as mp
import time
import gc

buttons = [False, False, False, False, False]
joint_angle = [0, 0, 0, 0, 0,0]
direction = [1, 1, 1, 1, 1,0]

import pandas as pdq

import time

import numpy as np
import cv2
import os
import sys
import traceback
import pandas as pd
import math

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
shapes = []


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

    sim.simxFinish(-1)


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




class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, image, draw=True):
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        image, hand, self.mpHands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, handNo=0, draw=True):
        x = []
        y = []
        h, w, c = image.shape
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, land in enumerate(myHand.landmark):
                cx, cy = int(land.x * w), int(land.y * h)
                x.append(cx)
                y.append(cy)

                if draw:
                    cv.circle(image, (cx, cy), 15, (0, 0, 255), cv.FILLED)

            self.button_condition(x, y)

            print(joint_angle)


        return x, y

    def button_condition(self, x, y):
        global buttons
        l = [8, 12, 16, 20]
        l_c = [7, 11, 15, 19]
        d = []
        d_c = []

        for i in range(0, 4):

            d.append(abs(x[l[i]] - x[0]) + abs(y[l[i]] - y[0]))
            d_c.append(abs(x[l_c[i]] - x[0]) + abs(y[l_c[i]] - y[0]))
            # print(d_1,d_c_1)
            if d[i] > d_c[i]:
                buttons[i] = True
                if joint_angle[i] < 90 and direction[i] == 1:
                    joint_angle[i] += direction[i]*2
                elif(joint_angle[i] > -90 and direction[i] == -1):
                    joint_angle[i] += direction[i]*2
                else:
                    direction[i] = -direction[i]



            else:
                buttons[i] = False





def main():
    url = "http://192.168.43.1:8080/video"
    cap = cv.VideoCapture(url)
    ret = 1
    pre_time = time.time()
    gc.enable()
    handDtc = handDetector()

    pickpos = False

    client_id = init_remote_api_server()
    print(client_id)

    time.sleep(1)
    JointHandler = []
    for i in range(6):
        print('NiryoOneJoint' + str(i + 1))
        code, handler = sim.simxGetObjectHandle(
            client_id, 'NiryoOneJoint' + str(i + 1), sim.simx_opmode_oneshot_wait)
        JointHandler.append(handler)



    return_code = start_simulation()

    print(return_code)

    start_time = 0

    object_pick_list = ['clock']

    while ret:
        crt_time = time.time()
        tt = int((crt_time - pre_time) * 1000)
        pre_time = crt_time
        fps = int((1 / tt) * 1000)

        ret, frame = cap.read()



        image = handDtc.findHands(frame)
        lmList = handDtc.findPosition(image)

        move_joint(JointHandler, joint_angle,'close')

        image = frame
        image = cv.resize(image, (500, 500))

        cv.putText(image, str(fps), (50, 50),
                   cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
        cv.imshow('image', image)
        pre_time = time.time()
        if cv.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            return_code = stop_simulation()

            ret = False
            # print(lmList)

        del image
        gc.collect()


if __name__ == "__main__":
    main()

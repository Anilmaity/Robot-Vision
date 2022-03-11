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
    code, visionSensorHandle = sim.simxGetObjectHandle(
        client_id, 'Vision_sensor', sim.simx_opmode_oneshot_wait)

    return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0,
                                                                                      sim.simx_opmode_streaming + 50)
    model = yolov5.load('yolov5s.pt')

    time.sleep(1)
    JointHandler = []
    for i in range(6):
        print('NiryoOneJoint' + str(i + 1))
        code, handler = sim.simxGetObjectHandle(
            client_id, 'NiryoOneJoint' + str(i + 1), sim.simx_opmode_oneshot_wait)
        JointHandler.append(handler)

    return_code = start_simulation()

    # move_joint(JointHandler, [0, 0, 0, 0, 0, 0], 'close')
    # angle_initiatializer = [0, 0, 0, 0, 0, 0]
    # positions_3d_with_gripper_directions = [[40, -20, 30, 'right'], [20, -20, 30, 'right'], [20, 20, 30, 'left'],
    #                                         [40, 20, 30, 'left'],
    #                                         [40, 20, 40, 'left'], [20, 20, 40, 'left'], [20, -20, 40, 'right'],
    #                                         [40, -20, 40, 'right'], [30, 1, 40, 'center']]
    # for pos in positions_3d_with_gripper_directions:
    #     time.sleep(10)
    #     angle_initiatializer = inverse_kinematics.get_robot_angles(
    #         pos[0], pos[1], pos[2], pos[3])



    start_time = 0

    object_pick_list = ['book']
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
                                                                                          sim.simx_opmode_buffer)

        img = transform_vision_sensor_image(
            vision_sensor_image, image_resolution, 1)

        results = model(img)
        result = results.pandas().xyxy[0]  # img1 predictions (pandas)
        rest = pd.DataFrame(result)
        # print(rest)
        object_ = ''
        for i, obj in enumerate(rest.iloc):
            # print(obj)
            # print((int(obj['xmin']), int(obj['ymin'])),(int(obj['xmax']), int(obj['ymax'])) )
            cv2.rectangle(img, (int(obj['xmin']), int(obj['ymin'])), (int(obj['xmax']), int(obj['ymax'])), (0, 0, 255),2)

            if (obj['name'] == object_pick_list[0]):
                object_ = obj['name']
                xposition = (obj['xmin'] + obj['xmax']) / 2
                yposition = (obj['ymin'] + obj['ymax']) / 2

            cv2.putText(img, obj['name'] + "  " + str(round(obj['confidence'], 1)),
                         (int(obj['xmin']), int(obj['ymin'])),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))


        cv2.putText(img, str(fps), (50, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

        if object_ == object_pick_list[0]:
            print(object_, xposition, yposition)
            if (xposition <= 250):
                move_joint(JointHandler, [0, -14, -30, -100, 78, 45], 'open')
                start_time = time.time()

        if (start_time != 0):
            if (time.time() - start_time > 4 and time.time() - start_time < 6):
                move_joint(JointHandler, [90, 0, 0, -100, 0, 0], 'open')

            if (time.time() - start_time > 6):
                move_joint(JointHandler, [90, 0, 0, -100, 0, 0], 'close')
                print("Complete 1 task")
                start_time = 0
                pickpos = False

        if (pickpos != True and object_ == object_pick_list[0]):
            move_joint(JointHandler, [0, -14, -30, -100, 78, 45], 'close')
            pickpos = True

        cv2.imshow('transformed image', img)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break

    cv2.destroyAllWindows()

    return_code = stop_simulation()

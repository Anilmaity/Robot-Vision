from cmath import sqrt
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

##############################################################

from inverse_kinematics import inverse_kinematics
import asyncio


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
    stretch_near = cv2.flip(stretch_near, 1)
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


async def move_robot(JointHandler):

    print('robot movement started')
    positions_3d_with_gripper_directions_static = [
        [30, 1, 40, 'right'], [30, 1, 40, 'left'], [30, 1, 40, 'center']]
    positions_3d_with_gripper_directions = [[40, -20, 30, 'right'], [20, -20, 30, 'right'], [20, 20, 30, 'left'], [40, 20, 30, 'left'],
                                            [40, 20, 40, 'left'], [20, 20, 40, 'left'], [20, -20, 40, 'right'], [40, -20, 40, 'right'], [30, 1, 40, 'center']]
    for pos in positions_3d_with_gripper_directions_static:
        await asyncio.sleep(10)
        angle_initiatializer = inverse_kinematics.get_robot_angles(
            pos[0], pos[1], pos[2], pos[3])
        print(angle_initiatializer)
        move_joint(JointHandler, angle_initiatializer, 'open')


async def process_vision_image(k):
    print('image processed')
    await asyncio.sleep(1)
    return k


async def start_object_detection():
    client_id = init_remote_api_server()
    print(client_id)
    JointHandler = []
    angle_initiatializer = [0, 0, 0, 0, 0, 0]

    code, visionSensorHandle = sim.simxGetObjectHandle(
        client_id, 'Vision_sensor', sim.simx_opmode_oneshot_wait)
    code2, visionSensor1Handle = sim.simxGetObjectHandle(
        client_id, 'Vision_sensor1', sim.simx_opmode_oneshot_wait)
    return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0,
                                                                                      sim.simx_opmode_streaming + 50)
    return_code, image_resolution1, vision_sensor1_image = sim.simxGetVisionSensorImage(client_id, visionSensor1Handle, 0,
                                                                                        sim.simx_opmode_streaming + 50)
    print(return_code, client_id)
    for i in range(6):
        print('NiryoOneJoint' + str(i + 1))
        code, handler = sim.simxGetObjectHandle(
            client_id, 'NiryoOneJoint' + str(i + 1), sim.simx_opmode_oneshot_wait)
        JointHandler.append(handler)

    return_code = start_simulation()
    move_joint(JointHandler, [0, 0, 0, 0, 0, 0], 'close')

    time.sleep(5)
    k = 0
    while(True):
        await asyncio.sleep(.01)

        if k == 10:
            task1 = asyncio.create_task(move_robot(JointHandler))
        k = k+2
        return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle,
                                                                                          0,
                                                                                          sim.simx_opmode_buffer)
        return_code1, image_resolution1, vision_sensor1_image = sim.simxGetVisionSensorImage(client_id, visionSensor1Handle,
                                                                                             0,
                                                                                             sim.simx_opmode_buffer)
        print(k)
        img = transform_vision_sensor_image(
            vision_sensor_image, image_resolution, 1)
        img2 = transform_vision_sensor_image(
            vision_sensor1_image, image_resolution1, 1)
        # concatanate image Horizontally
        all_sensor_images = np.concatenate((img, img2), axis=1)
        cv2.imshow('transformed image', all_sensor_images)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break
    cv2.destroyAllWindows()

    return_code = stop_simulation()


if __name__ == "__main__":

    asyncio.run(start_object_detection())

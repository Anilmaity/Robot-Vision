#importing project libraries


import time

import numpy as np
import cv2
import os, sys
import traceback
from object_pick_and_place import setRobot, resetPosition
# from simulation.object_pick_and_place import setRobot




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
    client_id = sim.simxStart("127.0.0.1", 19997, True, True, 5000, 5)  # start aconnection

    ##################################################

    return client_id


def start_simulation():
    global client_id

    return_code = 0

    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot_wait)


    return return_code


def transform_vision_sensor_image(vision_sensor_image, image_resolution,scaling):
    transformed_image = None

    ##############	ADD YOUR CODE HERE	##############

    transformed_image = np.array(vision_sensor_image, dtype=np.uint8)
    transformed_image.resize([image_resolution[0], (image_resolution[1]), 3])

    stretch_near = cv2.resize(transformed_image, (scaling*image_resolution[1],(image_resolution[1])*scaling),
                              interpolation=cv2.INTER_NEAREST)

    stretch_near = cv2.cvtColor(stretch_near, cv2.COLOR_BGR2RGB)
    stretch_near = cv2.flip(stretch_near, 0)

    ##################################################

    return stretch_near


def stop_simulation():
    global client_id

    return_code = 0

    ##############	ADD YOUR CODE HERE	##############

    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot_wait)

    ##################################################

    return return_code



def exit_remote_api_server():
    global client_id

    ##############	ADD YOUR CODE HERE	##############

    sim.simxFinish(-1)


if __name__ == "__main__":

    client_id = init_remote_api_server()
    print(client_id)
    return_code = start_simulation()
    code0, visionSensorHandle = sim.simxGetObjectHandle(client_id, 'vision_sensor', sim.simx_opmode_oneshot_wait)
    code1, handle_value1 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint1', sim.simx_opmode_blocking)
    code2, handle_value2 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint2', sim.simx_opmode_blocking)
    code3, handle_value3 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint3', sim.simx_opmode_blocking)
    code4, handle_value4 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint4', sim.simx_opmode_blocking)
    code5, handle_value5 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint5', sim.simx_opmode_blocking)
    code6, handle_value6 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint6', sim.simx_opmode_blocking)
    # print(vision_sensor_image)

    # while True:
    #     joint = int(input("joint (0-6) : "))

    #     if joint <= 7:
    #         degree = int(input("degree : "))
    #         control_joints(joint,degree)
    #     else:
    #         break

    # control_joints(1,1)
    # vision_sensor_image, image_resolution, return_code = get_vision_sensor_image()
    # return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0, sim.simx_opmode_streaming + 10)
    # time.sleep(1)

    link = 0
    setRobot(client_id, 15, 1,  handle_value1, handle_value2, handle_value3, handle_value4, handle_value5, handle_value6)
    while link!=20:
        link = int(input("enter link number"))
        joint_angle =  int(input('enter joint angle'))
        setRobot(client_id, link, joint_angle, handle_value1, handle_value2, handle_value3, handle_value4, handle_value5, handle_value6)
  

    # while True:
    #     crt_time = time.time()
    #     tt = int((crt_time - pre_time) * 1000)
    #     pre_time = crt_time
    #     fps = int((1/tt)*1000)

        '''
        joint = int(input("joint (0-6) : "))

        if joint <= 7:
            degree = int(input("degree : "))
            control_joints(joint, degree)
        else:
            break
        '''

        # return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle,
        #                                                                                   0,
        #                                                                                   sim.simx_opmode_buffer)
        # img = transform_vision_sensor_image(vision_sensor_image, image_resolution,2)
        # cv2.putText(img, str(fps), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0))
        # cv2.imshow('transformed image', img)
        # q = cv2.waitKey(1)
        # if q == ord("q"):
        #     break

    # cv2.destroyAllWindows()
    resetPosition(client_id,  handle_value1, handle_value2, handle_value3, handle_value4, handle_value5, handle_value6)
    time.sleep(6)
    stop_simulation()
    return_code = stop_simulation()
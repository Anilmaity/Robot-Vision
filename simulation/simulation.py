import time

import numpy as np
import cv2
import os, sys
import traceback
from object_pick_and_place import PickObject
##############################################################


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

    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_blocking)
    time.sleep(0.5)
    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)

    return return_code


def get_vision_sensor_image():
    global client_id

    vision_sensor_image = []
    image_resolution = []
    return_code = 0

    ##############	ADD YOUR CODE HERE	##############

    # Get the handle of vision sensor
    code, visionSensorHandle = sim.simxGetObjectHandle(client_id, 'vision_sensor', sim.simx_opmode_blocking)

    # Get the image of vision sensor
    return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0,
                                                                                      sim.simx_opmode_streaming)

    time.sleep(2)
    return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, visionSensorHandle, 0,
                                                                                      sim.simx_opmode_buffer)

    ##################################################

    return vision_sensor_image, image_resolution, return_code


def transform_vision_sensor_image(vision_sensor_image, image_resolution):
    transformed_image = None

    ##############	ADD YOUR CODE HERE	##############

    transformed_image = np.array(vision_sensor_image, dtype=np.uint8)
    transformed_image.resize([image_resolution[0], image_resolution[1], 3])

    transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)
    transformed_image = cv2.flip(transformed_image, 0)

    ##################################################

    return transformed_image


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


# def get_joints():
#     code ,position=sim.simxGetJointPosition(clientID, jointHandle, operationMode)
    
#     print()

def control_joints(joint , degree):

    # response_code, joint_position = sim.simxGetJointPosition(client_id,handle_value, sim.simx_opmode_streaming)
    # a = sim.simxSetObjectPosition(client_id,handle_value, -1, (12,0,0), sim.simx_opmode_oneshot)    
    # code, handle_value = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint1', sim.simx_opmode_oneshot_wait)    
    # # returnCode=sim.simxSetJointTargetVelocity(client_id,handle_value,1,sim.simx_opmode_streaming)
    # response_value = sim.simxSetJointTargetPosition(client_id, handle_value, 90*3.14/180, sim.simx_opmode_streaming)
    # print(code,handle_value, response_value)
    
    for i in range(5):
        code, handle_value = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint'+str(i+1), sim.simx_opmode_oneshot_wait)
        print(code,handle_value)
        response_value = sim.simxSetJointTargetPosition(client_id, handle_value, 90*3.14/180, sim.simx_opmode_streaming+500)
        # code = sim.simxSetJointPosition(client_id, handle_value, 90*3.14/180, sim.simx_opmode_oneshot_wait+200)
        print('setting_code', code)
       
    
    time.sleep(3)


    

    return 1


if __name__ == "__main__":

    client_id = init_remote_api_server()
    print(client_id)
    return_code = start_simulation()

    # print(vision_sensor_image)

    # while True:
    #     joint = int(input("joint (0-6) : "))

    #     if joint <= 7:
    #         degree = int(input("degree : "))
    #         control_joints(joint,degree)
    #     else:
    #         break

    PickObject(client_id)
    # control_joints(1,1)
    vision_sensor_image, image_resolution, return_code = get_vision_sensor_image()



    img = transform_vision_sensor_image(vision_sensor_image,image_resolution)
    cv2.imshow('transformed image',img )
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return_code = stop_simulation()


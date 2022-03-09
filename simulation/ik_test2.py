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
    move_joint(JointHandler, [0, 0, 0, 0, 0, 0], 'close')

    start_time = 0

    object_pick_list = ['book']
    angle_initiatializer = [0, 0, 0, 0, 0, 0]
    x_z_plane_positions = [[10, 20], [10, 50], [40, 50], [40, 20], [30, 40]]
    # positions = [[-20, 20], [-20, 50], [20, 50], [20, 20], [0, 40]]
    x_y_plane_positions = [[50, -20], [20, -20], [20, 20], [50, 20], [30, 0]]
    positions_3d = [[40, -20, 30], [20, -20, 30], [20, 20, 30], [40, 20, 30],
                    [40, 20, 40], [20, 20, 40], [20, -20, 40], [40, -20, 40], [30, 1, 40]]
    positions_3d_with_gripper_directions = [[40, -20, 30, 'right'], [20, -20, 30, 'right'], [20, 20, 30, 'left'], [40, 20, 30, 'left'],
                                            [40, 20, 40, 'left'], [20, 20, 40, 'left'], [20, -20, 40, 'right'], [40, -20, 40, 'right'], [30, 1, 40, 'center']]
    for pos in positions_3d_with_gripper_directions:
        time.sleep(5)
        angle_initiatializer = inverse_kinematics.get_robot_angles(
            pos[0], pos[1], pos[2], pos[3])
        print(angle_initiatializer)
        # given_x_position = pos[0]
        # given_y_position = pos[1]
        # given_z_position = pos[2]
        # x_position = given_x_position
        # y_position = given_y_position
        # z_position = given_z_position - 10
        # a1 = 30
        # a2 = 30

        # r1 = np.sqrt(x_position*x_position + z_position*z_position)
        # phi_1 = np.arctan(z_position/x_position)

        # print('r1', r1)
        # print('phi 1', phi_1*180/3.14)

        # phi_2 = np.arccos((a1*a1 + r1*r1 - a2*a2) / (2 * a1 * r1))

        # print('phi 2', phi_2*180/3.14)
        # theta_1 = phi_1 + phi_2
        # print('theta 1', 90 - theta_1*180/3.14)

        # phi_3 = np.arccos((a1*a1 - r1*r1 + a2*a2) / (2 * a1 * a2))

        # theta_2 = phi_3*180/3.14 - 90

        # print('theta 2',  theta_2)

        # theta_0 = np.arctan(y_position/x_position)

        # angle_initiatializer = [0, 0, 0, 0, 0, 0]

        # # move_joint(JointHandler, angle_initiatializer, 'open')

        # # Servo (joint) angles in degrees
        # servo_0_angle = theta_0*180/3.14  # Joint 1
        # servo_1_angle = -(90 - theta_1*180/3.14)  # Joint 2
        # servo_2_angle = 0  # Joint 3
        # servo_3_angle = theta_2  # Joint 4
        # servo_4_angle = 0  # Joint 5

        # # This servo would open and close the gripper (end-effector)
        # servo_5_angle = 0  # Joint 6

        # # Convert servo angles from degrees to radians
        # servo_0_angle = np.deg2rad(servo_0_angle)
        # servo_1_angle = np.deg2rad(servo_1_angle)
        # servo_2_angle = np.deg2rad(servo_2_angle)
        # servo_3_angle = np.deg2rad(servo_3_angle)
        # servo_4_angle = np.deg2rad(servo_4_angle)
        # servo_5_angle = np.deg2rad(servo_5_angle)

        # # This matrix helps convert the servo_1 frame to the servo_0 frame.
        # rot_mat_0_1 = np.array([[np.cos(servo_0_angle), 0, np.sin(servo_0_angle)],
        #                         [np.sin(servo_0_angle), 0, -
        #                             np.cos(servo_0_angle)],
        #                         [0, 1, 0]])

        # # This matrix helps convert the servo_2 frame to the servo_1 frame.
        # rot_mat_1_2 = np.array([[np.cos(servo_1_angle), -np.sin(servo_1_angle), 0],
        #                         [np.sin(servo_1_angle), np.cos(
        #                             servo_1_angle), 0],
        #                         [0, 0, 1]])

        # # This matrix helps convert the servo_3 frame to the servo_2 frame.
        # rot_mat_2_3 = np.array([[np.cos(servo_2_angle), -np.sin(servo_2_angle), 0],
        #                         [np.sin(servo_2_angle), np.cos(
        #                             servo_2_angle), 0],
        #                         [0, 0, 1]])

        # # This matrix helps convert the servo_4 frame to the servo_3 frame.
        # rot_mat_3_4 = np.array([[-np.sin(servo_3_angle), 0, np.cos(servo_3_angle)],
        #                         [np.cos(servo_3_angle), 0,
        #                             np.sin(servo_3_angle)],
        #                         [0, 1, 0]])

        # # This matrix helps convert the servo_5 frame to the servo_4 frame.
        # rot_mat_4_5 = np.array([[np.cos(servo_4_angle), -np.sin(servo_4_angle), 0],
        #                         [np.sin(servo_4_angle), np.cos(
        #                             servo_4_angle), 0],
        #                         [0, 0, 1]])

        # # Calculate the rotation matrix that converts the
        # # end-effector frame (frame 5) to the servo_0 frame.
        # # rot_mat_0_5 = rot_mat_0_1 @ rot_mat_1_2 @ rot_mat_2_3 @ rot_mat_3_4 @ rot_mat_4_5

        # rot_mat_0_3 = rot_mat_0_1 @ rot_mat_1_2  @ rot_mat_3_4

        # rot_mat_0_6 = np.array([[0.0, 1.0, 0.0],
        #                         [1.0, 0.0, 0.0],
        #                         [0.0, 0.0, -1.0]])

        # # Display the rotation matrix
        # # print(rot_mat_0_3)

        # inv_rot_mat_0_3 = np.linalg.inv(rot_mat_0_3)

        # # print('inversde rotation matrix', inv_rot_mat_0_3)

        # # Calculate the 3x3 rotation matrix of frame 6 relative to frame 3
        # rot_mat_3_6 = inv_rot_mat_0_3 @ rot_mat_0_6
        # # print(f'rot_mat_3_6 = {rot_mat_3_6}')

        # theta_5 = -np.arccos(rot_mat_3_6[2, 1])

        # print('theta 5', theta_5*180/3.14)

        # theta_6 = -np.arccos(rot_mat_3_6[2, 2] / np.sin(theta_5))

        # print('theta 6', theta_6*180/3.14)

        # if theta_6*180/3.14 >= 120:
        #     updated_theta6 = 120
        # elif theta_6*180/3.14 <= -120:
        #     updated_theta6 = -120
        # else:
        #     updated_theta6 = theta_6*180/3.14

        # theta_4 = np.arccos(rot_mat_3_6[0, 1] / np.sin(theta_5))

        # print('theta 4', theta_4*180/3.14)

        # angle_initiatializer = [1, 1, 0, 0, 0, 0]
        # angle_initiatializer[4] = theta_5*180/3.14
        # angle_initiatializer[5] = updated_theta6
        # angle_initiatializer[3] = theta_4*180/3.14
        # angle_initiatializer[0] = theta_0*180/3.14
        # angle_initiatializer[1] = -(90 - theta_1*180/3.14)
        # angle_initiatializer[2] = theta_2
        # print(angle_initiatializer)
        # angle_initiatializer[5] = pos
        move_joint(JointHandler, angle_initiatializer, 'open')
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

        # results = model(img)
        # result = results.pandas().xyxy[0]  # img1 predictions (pandas)
        # rest = pd.DataFrame(result)
        # print(rest)
        object_ = ''
        # for i, obj in enumerate(rest.iloc):
        # print(obj)
        # print((int(obj['xmin']), int(obj['ymin'])),(int(obj['xmax']), int(obj['ymax'])) )
        # cv2.rectangle(img, (int(obj['xmin']), int(obj['ymin'])), (int(obj['xmax']), int(obj['ymax'])), (0, 0, 255),
        #               2)

        # if (obj['name'] == object_pick_list[0]):
        #     object_ = obj['name']
        #     xposition = (obj['xmin'] + obj['xmax']) / 2
        #     yposition = (obj['ymin'] + obj['ymax']) / 2

        # cv2.putText(img, obj['name'] + "  " + str(round(obj['confidence'], 1)),
        #             (int(obj['xmin']), int(obj['ymin'])),
        #             cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
        # cv2.putText(img, str(fps), (50, 50),
        #             cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

        # if object_ == object_pick_list[0]:
        # print(object_, xposition, yposition)

        move_joint(JointHandler, angle_initiatializer, 'open')

        cv2.imshow('transformed image', img)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break

    cv2.destroyAllWindows()

    return_code = stop_simulation()

from re import T
from turtle import position
import numpy as np


def get_position_angles(x_position, y_position, z_position):

    position_angles = [0, 0, 0]
    a1 = 30
    a2 = 30
    r1 = np.sqrt(x_position*x_position + z_position*z_position)
    phi_1 = np.arctan(z_position/x_position)

    # print('r1', r1)
    # print('phi 1', phi_1*180/3.14)

    phi_2 = np.arccos((a1*a1 + r1*r1 - a2*a2) / (2 * a1 * r1))

    # print('phi 2', phi_2*180/3.14)
    theta_1 = phi_1 + phi_2
    # print('theta 1', 90 - theta_1*180/3.14)

    phi_3 = np.arccos((a1*a1 - r1*r1 + a2*a2) / (2 * a1 * a2))

    theta_2 = phi_3*180/3.14 - 90

    # print('theta 2',  theta_2)

    theta_0 = np.arctan(y_position/x_position)

    # angle_initiatializer = [0, 0, 0, 0, 0, 0]

    position_angles[0] = theta_0*180/3.14
    position_angles[1] = -(90 - theta_1*180/3.14)
    position_angles[2] = theta_2

    return position_angles


def get_orientation_angles(theta_0, theta_1, theta_2):
    orientation_angles = [0, 0, 0]

    # Servo (joint) angles in degrees
    servo_0_angle = theta_0  # Joint 1
    servo_1_angle = theta_1  # Joint 2
    servo_2_angle = 0  # Joint 3
    servo_3_angle = theta_2  # Joint 4
    servo_4_angle = 0  # Joint 5

    # This servo would open and close the gripper (end-effector)
    servo_5_angle = 0  # Joint 6

    # Convert servo angles from degrees to radians
    servo_0_angle = np.deg2rad(servo_0_angle)
    servo_1_angle = np.deg2rad(servo_1_angle)
    servo_2_angle = np.deg2rad(servo_2_angle)
    servo_3_angle = np.deg2rad(servo_3_angle)
    servo_4_angle = np.deg2rad(servo_4_angle)
    servo_5_angle = np.deg2rad(servo_5_angle)

    # This matrix helps convert the servo_1 frame to the servo_0 frame.
    rot_mat_0_1 = np.array([[np.cos(servo_0_angle), 0, np.sin(servo_0_angle)],
                            [np.sin(servo_0_angle), 0, -
                             np.cos(servo_0_angle)],
                            [0, 1, 0]])

    # This matrix helps convert the servo_2 frame to the servo_1 frame.
    rot_mat_1_2 = np.array([[np.cos(servo_1_angle), -np.sin(servo_1_angle), 0],
                            [np.sin(servo_1_angle), np.cos(
                                servo_1_angle), 0],
                            [0, 0, 1]])

    # This matrix helps convert the servo_3 frame to the servo_2 frame.
    rot_mat_2_3 = np.array([[np.cos(servo_2_angle), -np.sin(servo_2_angle), 0],
                            [np.sin(servo_2_angle), np.cos(
                                servo_2_angle), 0],
                            [0, 0, 1]])

    # This matrix helps convert the servo_4 frame to the servo_3 frame.
    rot_mat_3_4 = np.array([[-np.sin(servo_3_angle), 0, np.cos(servo_3_angle)],
                            [np.cos(servo_3_angle), 0,
                             np.sin(servo_3_angle)],
                            [0, 1, 0]])

    # This matrix helps convert the servo_5 frame to the servo_4 frame.
    rot_mat_4_5 = np.array([[np.cos(servo_4_angle), -np.sin(servo_4_angle), 0],
                            [np.sin(servo_4_angle), np.cos(
                                servo_4_angle), 0],
                            [0, 0, 1]])

    # Calculate the rotation matrix that converts the
    # end-effector frame (frame 5) to the servo_0 frame.
    # rot_mat_0_5 = rot_mat_0_1 @ rot_mat_1_2 @ rot_mat_2_3 @ rot_mat_3_4 @ rot_mat_4_5

    rot_mat_0_3 = rot_mat_0_1 @ rot_mat_1_2  @ rot_mat_3_4

    rot_mat_0_6 = np.array([[0.0, 1.0, 0.0],
                            [1.0, 0.0, 0.0],
                            [0.0, 0.0, -1.0]])

    # Display the rotation matrix
    # print(rot_mat_0_3)

    inv_rot_mat_0_3 = np.linalg.inv(rot_mat_0_3)

    # print('inversde rotation matrix', inv_rot_mat_0_3)

    # Calculate the 3x3 rotation matrix of frame 6 relative to frame 3
    rot_mat_3_6 = inv_rot_mat_0_3 @ rot_mat_0_6
    # print(f'rot_mat_3_6 = {rot_mat_3_6}')

    theta_5 = -np.arccos(rot_mat_3_6[2, 1])

    # print('theta 5', theta_5*180/3.14)

    theta_6 = -np.arccos(rot_mat_3_6[2, 2] / np.sin(theta_5))

    # print('theta 6', theta_6*180/3.14)

    if theta_6*180/3.14 >= 120:
        updated_theta6 = 120
    elif theta_6*180/3.14 <= -120:
        updated_theta6 = -120
    else:
        updated_theta6 = theta_6*180/3.14

    theta_4 = np.arccos(rot_mat_3_6[0, 1] / np.sin(theta_5))

    # print('theta 4', theta_4*180/3.14)
    orientation_angles[1] = theta_5*180/3.14
    orientation_angles[2] = updated_theta6
    orientation_angles[0] = theta_4*180/3.14

    return orientation_angles


def get_updated_orientation_angles(theta_0_1, theta_1, theta_2, gripper_direction):
    orientation_angles = [0, 0, 0]

    joint_0_angle = theta_0_1
    joint_1_angle = theta_1
    joint_2_angle = theta_2
    # print(joint_4_angle, theta_1, theta_2)
    joint_0_angle = np.deg2rad(joint_0_angle)
    joint_1_angle = np.deg2rad(joint_1_angle)
    joint_2_angle = np.deg2rad(joint_2_angle)

    rot_mat_0_1 = np.array([[np.cos(joint_0_angle), 0, np.sin(joint_0_angle)],
                            [np.sin(joint_0_angle), 0, -np.cos(joint_0_angle)],
                            [0, 1, 0]])
    # print('rot mat 01', rot_mat_0_1)

    rot_mat_1_2 = np.array([[-np.sin(joint_1_angle), -np.cos(joint_1_angle), 0],
                            [np.cos(joint_1_angle),  -
                             np.sin(joint_1_angle), 0],
                            [0, 0, 1]])
    # print('rot mat 12', rot_mat_1_2)

    rot_mat_2_3 = np.array([[np.cos(joint_2_angle), 0, np.sin(joint_2_angle)],
                            [np.sin(joint_2_angle), 0, -
                             np.cos(joint_2_angle)],
                            [0, 1, 0]])

    # print('rot mat 12', rot_mat_2_3)

    rot_mat_0_3 = rot_mat_0_1 @ rot_mat_1_2 @ rot_mat_2_3
    # print('rot mat 03', rot_mat_0_3)

    rot_mat_0_6 = np.array([[0.0, 0.0, 1.0],
                            [0.0, -1.0, 0.0],
                            [1.0, 0.0, 0.0]])

    if gripper_direction == 'left':
        rot_mat_0_6 = np.array([[0.0, 1.0, 0.0],
                                [0.0, 0.0, 1.0],
                                [1.0, 0.0, 0.0]])
    elif gripper_direction == 'right':
        rot_mat_0_6 = np.array([[0.0, -1.0, 0.0],
                                [0.0, 0.0, -1.0],
                                [1.0, 0.0, 0.0]])
    else:
        rot_mat_0_6 = np.array([[0.0, 0.0, 1.0],
                                [0.0, -1.0, 0.0],
                                [1.0, 0.0, 0.0]])

    inv_rot_mat_0_3 = np.linalg.inv(rot_mat_0_3)

    rot_mat_3_6 = inv_rot_mat_0_3 @ rot_mat_0_6

    theta_5 = np.arccos(rot_mat_3_6[2, 2])
    # print('theta_5', theta_5)
    #
    # print('theta_5', theta_5*180/3.14)
    # print('theta 32', rot_mat_3_6[2, 1])

    theta_6 = np.arcsin(rot_mat_3_6[2, 1]/np.sin(theta_5))
    #
    # print('theta_6', theta_6*180/3.14)

    theta_4 = np.arcsin(rot_mat_3_6[1, 2]/np.sin(theta_5))
    #
    # print('theta_4', theta_4*180/3.14)
    #
    # print(joint_0_angle, joint_1_angle, joint_2_angle)

    # Check that the angles we calculated result in a valid rotation matrix
    r11 = np.cos(theta_4) * np.cos(theta_5) * np.cos(theta_6) - \
        np.sin(theta_4) * np.sin(theta_6)
    r12 = -np.cos(theta_4) * np.cos(theta_5) * np.sin(theta_6) - \
        np.sin(theta_4) * np.cos(theta_6)
    r13 = np.cos(theta_4) * np.sin(theta_5)
    r21 = np.sin(theta_4) * np.cos(theta_5) * np.cos(theta_6) + \
        np.cos(theta_4) * np.sin(theta_6)
    r22 = -np.sin(theta_4) * np.cos(theta_5) * np.sin(theta_6) + \
        np.cos(theta_4) * np.cos(theta_6)
    r23 = np.sin(theta_4) * np.sin(theta_5)
    r31 = -np.sin(theta_5) * np.cos(theta_6)
    r32 = np.sin(theta_5) * np.sin(theta_6)
    r33 = np.cos(theta_5)

    check_rot_mat_3_6 = np.array([[r11, r12, r13],
                                  [r21, r22, r23],
                                  [r31, r32, r33]])

    #print('check rot_3_6 matrix', check_rot_mat_3_6)

    orientation_angles[0] = theta_4*180/3.14
    orientation_angles[1] = theta_5*180/3.14
    orientation_angles[2] = theta_6*180/3.14

    return orientation_angles


def get_robot_angles(x_given_position, y_given_position, z_given_position, gripper_orientation):

    x_position = x_given_position
    y_position = y_given_position
    z_position = z_given_position - 10
    a1 = 30
    a2 = 30

    position_angles = get_position_angles(x_position, y_position, z_position)

    # orientation_angles = get_orientation_angles(
    #     position_angles[0], position_angles[1], position_angles[2])

    orientation_angles = get_updated_orientation_angles(
        position_angles[0], position_angles[1], position_angles[2], gripper_orientation)

    calc_joint_angles = [0, 0, 0, 0, 0, 0]
    calc_joint_angles[0] = position_angles[0]
    calc_joint_angles[1] = position_angles[1]
    calc_joint_angles[2] = position_angles[2]
    calc_joint_angles[3] = orientation_angles[0]
    calc_joint_angles[4] = orientation_angles[1]
    calc_joint_angles[5] = orientation_angles[2]

    # print(position_angles, 'position_angles')
    # print(orientation_angles, 'orientation angles')

    return calc_joint_angles


# get_robot_angles(1, 30, 40)

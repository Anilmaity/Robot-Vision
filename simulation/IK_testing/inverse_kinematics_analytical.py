import numpy as np  # Scientific computing library

# Project: Calculating Rotation Matrices for a 6 DOF Robotic Arm
# Author: Addison Sears-Collins
# Date created: August 6, 2020

# Servo (joint) angles in degrees
servo_0_angle = 0  # Joint 1
servo_1_angle = 90  # Joint 2
servo_2_angle = 0  # Joint 3
servo_3_angle = 0  # Joint 4
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
                        [np.sin(servo_0_angle), 0, -np.cos(servo_0_angle)],
                        [0, 1, 0]])

# This matrix helps convert the servo_2 frame to the servo_1 frame.
rot_mat_1_2 = np.array([[np.cos(servo_1_angle), -np.sin(servo_1_angle), 0],
                        [np.sin(servo_1_angle), np.cos(servo_1_angle), 0],
                        [0, 0, 1]])

# This matrix helps convert the servo_3 frame to the servo_2 frame.
rot_mat_2_3 = np.array([[np.cos(servo_2_angle), -np.sin(servo_2_angle), 0],
                        [np.sin(servo_2_angle), np.cos(servo_2_angle), 0],
                        [0, 0, 1]])

# This matrix helps convert the servo_4 frame to the servo_3 frame.
rot_mat_3_4 = np.array([[-np.sin(servo_3_angle), 0, np.cos(servo_3_angle)],
                        [np.cos(servo_3_angle), 0, np.sin(servo_3_angle)],
                        [0, 1, 0]])

# This matrix helps convert the servo_5 frame to the servo_4 frame.
rot_mat_4_5 = np.array([[np.cos(servo_4_angle), -np.sin(servo_4_angle), 0],
                        [np.sin(servo_4_angle), np.cos(servo_4_angle), 0],
                        [0, 0, 1]])

# Calculate the rotation matrix that converts the
# end-effector frame (frame 5) to the servo_0 frame.
# rot_mat_0_5 = rot_mat_0_1 @ rot_mat_1_2 @ rot_mat_2_3 @ rot_mat_3_4 @ rot_mat_4_5

rot_mat_0_3 = rot_mat_0_1 @ rot_mat_1_2  @ rot_mat_3_4

rot_mat_0_6 = np.array([[0.0, 1.0, 0.0],
                        [-1.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0]])

# Display the rotation matrix
print(rot_mat_0_3)


inv_rot_mat_0_3 = np.linalg.inv(rot_mat_0_3)

# print('inversde rotation matrix', inv_rot_mat_0_3)

# Calculate the 3x3 rotation matrix of frame 6 relative to frame 3
rot_mat_3_6 = inv_rot_mat_0_3 @ rot_mat_0_6
# print(f'rot_mat_3_6 = {rot_mat_3_6}')

theta_5 = np.arccos(rot_mat_3_6[2, 1])

# print('theta 5', theta_5*180/3.14)


given_x_position = 30
given_z_position = 40
given_y_position = 30
x_position = given_x_position
z_position = given_z_position - 10
y_position = given_y_position

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

theta_0_deg = theta_0*180/3.14

# print('theta 0',  theta_0_deg)


row_value = 0.003

angle_value = np.arccos(0.99944)

print('angle value', np.arcsin(row_value/np.sin(angle_value))*180/3.14)


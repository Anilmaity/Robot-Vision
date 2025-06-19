import time
import math
import pybullet as p
import pybullet_data

# Connect to PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

robot = p.loadURDF("niryo.urdf", useFixedBase=True)

end_effector_index = 6  # Change if needed

# Get movable joints (only revolute and prismatic, limit to 6 DoF)
movable_joints = []
for joint_index in range(p.getNumJoints(robot)):
    joint_info = p.getJointInfo(robot, joint_index)
    joint_type = joint_info[2]
    if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC] and len(movable_joints) < 6:
        movable_joints.append(joint_index)

print("Movable joints:", movable_joints)

# Define circular path parameters (along Z-Y plane)
radius = 0.10  # 20 cm
center_y = 0.2
center_z = 0.2
fixed_x = 0.0
num_points = 100  # Total points in the circle
duration = 20  # Total duration in seconds for one complete circle
sleep_time = duration / num_points

print("\n--- Starting Circular Motion ---\n")

for i in range(num_points + 1):  # +1 to complete the circle
    theta = (2 * math.pi * i) / num_points  # Angle in radians
    target_y = center_y + radius * math.cos(theta)
    target_z = center_z + radius * math.sin(theta)
    target_pos = [fixed_x, target_y, target_z]

    # Compute IK for the target position
    joint_angles = p.calculateInverseKinematics(robot, end_effector_index, target_pos)

    # Convert to degrees and limit to movable joints
    joint_angles_deg = [math.degrees(angle) for angle in joint_angles[:len(movable_joints)]]

    print(f"Step {i+1}: Target Pos = {target_pos}")
    print(f"Joint Angles (Degrees): {joint_angles_deg}\n")

    # Apply IK solution to each movable joint
    for j, joint_index in enumerate(movable_joints):
        p.setJointMotorControl2(robot,
                                joint_index,
                                p.POSITION_CONTROL,
                                targetPosition=joint_angles[j])

    # Step simulation
    for _ in range(10):
        p.stepSimulation()
        time.sleep(1.0 / 240.0)

    time.sleep(sleep_time)

print("\n--- Circular Motion Completed ---\n")

# Hold final position
time.sleep(5)

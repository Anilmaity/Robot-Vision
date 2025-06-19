import time
import math
import pybullet as p
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

robot = p.loadURDF("niryo.urdf", useFixedBase=True)

target_positions = [
    [0.0, 0.1, 0.4],
    [0.0, 0.1, 0.6],
    [0.0, 0.1, 0.8]
]

end_effector_index = 12  # May change per your URDF

# Get movable (revolute/prismatic) joint indices
movable_joints = []
for joint_index in range(p.getNumJoints(robot)):
    joint_info = p.getJointInfo(robot, joint_index)
    joint_type = joint_info[2]
    if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
        movable_joints.append(joint_index)

print("Movable joints:", movable_joints)

for idx, target_pos in enumerate(target_positions):
    joint_angles = p.calculateInverseKinematics(robot, end_effector_index, target_pos)

    # Convert to degrees
    joint_angles_deg = [math.degrees(angle) for angle in joint_angles[:len(movable_joints)]]

    print(f"\nTarget Position {idx+1}: {target_pos}")
    print(f"Joint Angles (Degrees): {joint_angles_deg}")

    # Apply IK result to movable joints only
    for i, joint_index in enumerate(movable_joints):
        p.setJointMotorControl2(robot,
                                joint_index,
                                p.POSITION_CONTROL,
                                targetPosition=joint_angles[i])

    for _ in range(100):
        p.stepSimulation()
        time.sleep(1.0/240.0)

    time.sleep(25)

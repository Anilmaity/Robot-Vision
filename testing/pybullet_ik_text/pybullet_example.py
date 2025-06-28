import time
import math
import pybullet as p
import pybullet_data
import serial


serial_connected = False
try:
    ser = serial.Serial('COM9', 1000000, timeout=1)
    time.sleep(3)  # Wait for Arduino to initialize
    print("Connected to Arduino on COM9")
    serial_connected = True
except:
    pass

def connect_pybullet(gui=True):
    """Connect to the PyBullet simulator."""
    if gui:
        p.connect(p.GUI)
    else:
        p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())


def load_robot(urdf_path="niryo.urdf", fixed_base=True):
    """Load the robot URDF into the simulation."""
    robot_id = p.loadURDF(urdf_path, useFixedBase=fixed_base)
    return robot_id


def get_movable_joints(robot_id, max_dof=6):
    """Retrieve indices of movable (revolute/prismatic) joints, limited to max_dof."""
    movable = []
    for joint_idx in range(p.getNumJoints(robot_id)):
        joint_info = p.getJointInfo(robot_id, joint_idx)
        joint_type = joint_info[2]
        if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC] and len(movable) < max_dof:
            movable.append(joint_idx)
    return movable


def compute_circular_path(radius, center, num_points, plane='yz'):
    """
    Generate a list of target positions forming a circular path.

    Args:
        radius (float): Circle radius.
        center (list): [x, y, z] center of the circle.
        num_points (int): Number of points to generate.
        plane (str): 'yz' or 'xy' plane.

    Returns:
        List of [x, y, z] target positions.
    """
    path = []
    for i in range(num_points + 1):
        theta = (2 * math.pi * i) / num_points
        if plane == 'yz':
            x = center[0]
            y = center[1] + radius * math.cos(theta)
            z = center[2] + radius * math.sin(theta)
        elif plane == 'xy':
            x = center[0] + radius * math.cos(theta)
            y = center[1] + radius * math.sin(theta)
            z = center[2]
        else:
            raise ValueError("Invalid plane. Use 'yz' or 'xy'.")
        path.append([x, y, z])
    return path


def send_command_arduino(angles):
    if serial_connected:
        M1  = angles[0]
        M2 = angles[1]
        M3 = angles[2]


        command = f"M1 {M1} M2 {-M2} M3 {-M3}\n"

        print(command)
        ser.write(command.encode())

        start_time = time.time()
        while True:
            # Check for timeout (e.g., 5 seconds)
            if time.time() - start_time > 5:
                print("Error: Timeout waiting for 'Done' response")
                # ser.close()
                return False

            # Read serial response
            response = ser.readline().decode().strip()
            if response == "Done":
                print("Received 'Done' from Arduino")
                # ser.close()
                return True

            # Small delay to prevent CPU overuse
            # time.sleep(0.01)





def move_robot_along_path(robot_id, end_effector_idx, movable_joints, path, duration):
    """
    Move robot along the given path.

    Args:
        robot_id (int): PyBullet robot unique ID.
        end_effector_idx (int): End-effector link index.
        movable_joints (list): Indices of movable joints.
        path (list): List of target positions.
        duration (float): Time in seconds to complete the path.
    """
    sleep_time = duration / len(path)

    for idx, target_pos in enumerate(path):
        joint_angles = p.calculateInverseKinematics(robot_id, end_effector_idx, target_pos)
        joint_angles_deg = [math.degrees(angle) for angle in joint_angles[:len(movable_joints)]]
        processed_deg = [round(angle, 0) for angle in joint_angles_deg]

        send_command_arduino(processed_deg)
        print(f"Step {idx + 1}: Target Pos = {target_pos}")



        for j, joint_idx in enumerate(movable_joints):
            p.setJointMotorControl2(robot_id,
                                    joint_idx,
                                    p.POSITION_CONTROL,
                                    targetPosition=joint_angles[j])
        # Smooth simulation steps
        for _ in range(10):
            p.stepSimulation()
            time.sleep(1.0 / 240.0)

        print("moved")

        # time.sleep(0.3)


def perform_circular_motion(revolutions=1, plane='yz'):
    """
    Perform circular motion of the robot end-effector in the specified plane.

    Args:
        revolutions (int): Number of complete circular revolutions.
        plane (str): 'yz' or 'xy' for the circular plane.
    """


    path = compute_circular_path(radius, center, num_points, plane=plane)

    print(f"\n--- Starting Circular Motion in {plane.upper()} Plane ---\n")
    for rev in range(revolutions):
        print(f"--- Revolution {rev + 1} ---")
        move_robot_along_path(robot_id, end_effector_idx, movable_joints, path, duration)

    print("\n--- Circular Motion Completed ---\n")
    time.sleep(1)  # Hold final pose


if __name__ == "__main__":
    # Run motion for 5 revolutions in the XY plane
    connect_pybullet(gui=True)
    robot_id = load_robot(urdf_path="niryo/niryo.urdf")
    end_effector_idx = 6  # Adjust if different
    movable_joints = get_movable_joints(robot_id)

    print("Movable Joints:", movable_joints)

    radius = 0.15  # 10 cm
    center = [0.0, 0.25, 0.15]  # Center coordinates
    num_points = 30
    duration = 5  # seconds per revolution

    # perform_circular_motion(revolutions=2, plane='xy')  # Change 'xy' to 'yz' for ZY plane
    perform_circular_motion(revolutions=30, plane='yz')  # Change 'xy' to 'yz' for ZY plane

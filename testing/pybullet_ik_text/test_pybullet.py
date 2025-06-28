import time

import pybullet as p
import pybullet_data
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF("niryo/niryo.urdf")
time.sleep(100)
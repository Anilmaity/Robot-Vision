import time
import sim
def setRobot(client_id,link, joint_angle):
    code, handle_value1 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint1', sim.simx_opmode_blocking)
    code, handle_value2 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint2', sim.simx_opmode_blocking)
    code, handle_value3 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint3', sim.simx_opmode_blocking)
    code, handle_value4 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint4', sim.simx_opmode_blocking)
    code, handle_value5 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint5', sim.simx_opmode_blocking)
    code, handle_value6 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint6', sim.simx_opmode_blocking)
    # print(handle_value1, handle_value2, handle_value3, handle_value4, handle_value5, handle_value6)
    chde, connection = sim.simxGetObjectHandle(client_id, 'NiryoOne_connection', sim.simx_opmode_oneshot_wait)
    che, gripperhand = sim.simxGetObjectHandle(client_id, 'NiryoLGripper', sim.simx_opmode_oneshot_wait)

    if link==1:
        sim.simxSetJointTargetPosition(client_id, handle_value1,joint_angle*3.14/180, sim.simx_opmode_oneshot)
    elif link==2:
        sim.simxSetJointTargetPosition(client_id, handle_value2, joint_angle*3.14/180, sim.simx_opmode_oneshot)
    elif link==3:
        sim.simxSetJointTargetPosition(client_id, handle_value3, joint_angle*3.14/180, sim.simx_opmode_oneshot)
    elif link==4:
        sim.simxSetJointTargetPosition(client_id, handle_value4, joint_angle*3.14/180, sim.simx_opmode_oneshot)
    elif link==5:
        sim.simxSetJointTargetPosition(client_id, handle_value5, joint_angle*3.14/180, sim.simx_opmode_oneshot)
    elif link==6:
        sim.simxSetJointTargetPosition(client_id, handle_value6, joint_angle*3.14/180, sim.simx_opmode_oneshot)
    elif link==10:
        sim.simxSetIntegerSignal(client_id,'NiryoLGripper_close' ,1,sim.simx_opmode_oneshot)
    elif link==11:
        sim.simxClearIntegerSignal(client_id, 'NiryoLGripper_close',sim.simx_opmode_oneshot)
    elif link==15:
        a = pickObject(client_id)
        print(a)
    elif link==16:
        a = placeObject(client_id)
        print(a)
    else:
        print('invalid selection')


    print('object picked')
    time.sleep(3)
    return 1


def pickObject(client_id):

    code, handle_value1 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint1', sim.simx_opmode_blocking)
    code, handle_value2 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint2', sim.simx_opmode_blocking)
    code, handle_value3 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint3', sim.simx_opmode_blocking)
    code, handle_value4 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint4', sim.simx_opmode_blocking)
    code, handle_value5 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint5', sim.simx_opmode_blocking)
    code, handle_value6 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint6', sim.simx_opmode_blocking)
 
    sim.simxSetJointTargetPosition(client_id, handle_value5,78*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value6,45*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value1,0*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value2,-14*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value3,-30*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value4,-100*3.14/180, sim.simx_opmode_oneshot)


    return 1


def placeObject(client_id):

    code, handle_value1 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint1', sim.simx_opmode_blocking)
    code, handle_value2 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint2', sim.simx_opmode_blocking)
    code, handle_value3 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint3', sim.simx_opmode_blocking)
    code, handle_value4 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint4', sim.simx_opmode_blocking)
    code, handle_value5 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint5', sim.simx_opmode_blocking)
    code, handle_value6 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint6', sim.simx_opmode_blocking)
 
    sim.simxSetJointTargetPosition(client_id, handle_value1,90*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value2,0*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value3,0*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value4,-100*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value5,0*3.14/180, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(client_id, handle_value6,00*3.14/180, sim.simx_opmode_oneshot)


    return 1
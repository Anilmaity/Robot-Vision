import time
import sim
def PickObject(client_id):
    code, handle_value1 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint1', sim.simx_opmode_oneshot_wait)
    code, handle_value2 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint2', sim.simx_opmode_oneshot_wait)
    code, handle_value3 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint3', sim.simx_opmode_oneshot_wait)
    code, handle_value4 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint4', sim.simx_opmode_oneshot_wait)
    code, handle_value5 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint5', sim.simx_opmode_oneshot_wait)
    code, handle_value6 = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint6', sim.simx_opmode_oneshot_wait)
    # print(handle_value1, handle_value2, handle_value3, handle_value4, handle_value5, handle_value6)
    
    
    sim.simxSetJointTargetPosition(client_id, handle_value2, 0*3.14/180, sim.simx_opmode_streaming+500)
    sim.simxSetJointTargetPosition(client_id, handle_value3, -10*3.14/180, sim.simx_opmode_streaming+500)
    sim.simxSetJointTargetPosition(client_id, handle_value5, -70*3.14/180, sim.simx_opmode_streaming+500)
    sim.simxSetJointTargetPosition(client_id, handle_value6, -90*3.14/180, sim.simx_opmode_streaming+500)
    sim.simxClearIntegerSignal(client_id, 'NiryoLGripper_close',sim.simx_opmode_oneshot)
    # sim.simxSetIntegerSignal(client_id, 'NiryoGripper_close',sim.simx_opmode_oneshot)
    # for i in range(5):
    #     code, handle_value = sim.simxGetObjectHandle(client_id, 'NiryoOneJoint'+str(i+1), sim.simx_opmode_oneshot_wait)
    #     print(code,handle_value)
    #     response_value = sim.simxSetJointTargetPosition(client_id, handle_value, 90*3.14/180, sim.simx_opmode_streaming+500)
    #     # code = sim.simxSetJointPosition(client_id, handle_value, 90*3.14/180, sim.simx_opmode_oneshot_wait+200)
    #     print('setting_code', code)
    print('object picked')
    time.sleep(3)
    return 1
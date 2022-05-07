import requests
import time
url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id_no': '00'}

joints =[0,0,0,0,0,0]


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

stepen = 26
stepper_sig_pin = [13,5,20]
stepper_dir_pin = [19,6,16]
GPIO.setup(stepen, GPIO.OUT)





def step_setup():
    for pin in stepper_sig_pin:
        GPIO.setup(pin, GPIO.OUT)
        print(pin)
    for pin in stepper_dir_pin:
        GPIO.setup(pin, GPIO.OUT)
        print(pin)
    GPIO.output(stepen, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(stepen, GPIO.LOW)


def step_run(steps, stepper_no):
    for i,stepper in  enumerate(stepper_no):
        if steps[i] >= 0:
            GPIO.output(stepper_dir_pin[stepper], GPIO.HIGH)
            for i in range(0, steps[i]):
                GPIO.output(stepper_sig_pin[stepper], GPIO.LOW)
                time.sleep(0.001)
                GPIO.output(stepper_sig_pin[stepper], GPIO.HIGH)
                time.sleep(0.001)
            print("complete_cw")

        elif steps[i] < 0:
            GPIO.output(stepper_dir_pin[stepper], GPIO.LOW)
            for i in range(0, abs(steps[i])):
                GPIO.output(stepper_sig_pin[stepper], GPIO.LOW)
                time.sleep(0.001)
                GPIO.output(stepper_sig_pin[stepper], GPIO.HIGH)
                time.sleep(0.001)
            print("complete_ccw")



step_setup()

while True:
    x = requests.post(url, data=myobj)
    data = x.json()

    stepper_delta_angle = [joints[0] - (data['stepper_1']*26) , joints[1] - (data['stepper_2']*26), joints[2] - (data['stepper_3']*26)]

    joints[0] = data['stepper_1']*26
    joints[1] = data['stepper_2']*26
    joints[2] = data['stepper_3']*26
    joints[3] = data['servo_1']
    joints[4] = data['servo_2']
    joints[5] = data['servo_3']

    step_run(stepper_delta_angle, [0,1,2])

    print(stepper_delta_angle)

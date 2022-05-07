import requests
import time
url = 'https://robotvision.herokuapp.com/get_angles/'
myobj = {'id_no': '00'}

joints =[0,0,0,0,0,0]



import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

stepen = 8
stepper_sig_pin = [7]
stepper_dir_pin = [1]
GPIO.setup(stepen, GPIO.OUT)





def step_setup():
    for pin in stepper_sig_pin:
        GPIO.setup(pin, GPIO.OUT)
    for pin in stepper_dir_pin:
        GPIO.setup(pin, GPIO.OUT)

    GPIO.output(stepen, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(stepen, GPIO.LOW)


def step_run(steps, stepper_no):
    for step in  steps:
        if step >= 0:
            GPIO.output(stepper_dir_pin[stepper_no], GPIO.HIGH)
            for i in range(0, 1):
                GPIO.output(stepper_sig_pin[stepper_no], GPIO.LOW)
                time.sleep(0.001)
                GPIO.output(stepper_sig_pin[stepper_no], GPIO.HIGH)
                time.sleep(0.001)

        elif step < 0:
            GPIO.output(stepper_dir_pin[stepper_no], GPIO.LOW)
            for i in range(0, steps):
                GPIO.output(stepper_sig_pin[stepper_no], GPIO.LOW)
                time.sleep(0.001)
                GPIO.output(stepper_sig_pin[stepper_no], GPIO.HIGH)
                time.sleep(0.001)


step_setup()

while True:
    x = requests.post(url, data=myobj)
    data = x.json()

    stepper_delta_angle = [joints[0] - data['stepper_1'] , joints[1] - data['stepper_2'], joints[2] - data['stepper_3']]

    joints[0] = data['stepper_1']
    joints[1] = data['stepper_2']
    joints[2] = data['stepper_3']
    joints[3] = data['servo_1']
    joints[4] = data['servo_2']
    joints[5] = data['servo_3']

    step_run(stepper_delta_angle, [0,1,2])

    print(stepper_delta_angle)

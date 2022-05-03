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
while(True):
    step_run(200, 0)
    time.sleep(0.5)
    step_run(200, 0)
    time.sleep(0.5)

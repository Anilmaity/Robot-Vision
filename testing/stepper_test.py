
import time
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
        print(stepper_dir_pin[stepper])
        print(stepper_sig_pin[stepper])

        print(steps[i])
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
    

    step_run([400], [2])
    time.sleep(1)
    step_run([-400], [2])



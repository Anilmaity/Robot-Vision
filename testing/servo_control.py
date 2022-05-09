# https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/
import RPi.GPIO as GPIO
import time



servopin = [1,7,8,25]# 1, 7, 8, 25
servolist = []
GPIO.setmode(GPIO.BCM)

for i, s_p in enumerate(servopin):
  GPIO.setup(s_p, GPIO.OUT)
  servolist.append(GPIO.PWM(s_p, 50)) # GPIO 17 for PWM with 50Hz
  servolist[i].start(2.5) # Initialization

try:
  while True:

    for serv in servolist:

      serv.ChangeDutyCycle(5)
      time.sleep(0.5)
      serv.ChangeDutyCycle(7.5)
      time.sleep(0.5)
      serv.ChangeDutyCycle(10)
      time.sleep(0.5)
      serv.ChangeDutyCycle(12.5)
      time.sleep(0.5)
      serv.ChangeDutyCycle(10)
      time.sleep(0.5)
      serv.ChangeDutyCycle(7.5)
      time.sleep(0.5)
      serv.ChangeDutyCycle(5)
      time.sleep(0.5)
      serv.ChangeDutyCycle(2.5)
      time.sleep(0.5)

except KeyboardInterrupt:
  for serv in servolist:
    serv.stop()
  GPIO.cleanup()


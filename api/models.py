from django.db import models

# Create your models here.

class Robot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    user_email = models.CharField(max_length=50,default='')
    username = models.CharField(max_length=50)
    id_no = models.CharField(max_length=25,default='')
    online = models.BooleanField(default=False)
    login = models.BooleanField(default=False)
    operating_status = models.BooleanField(default=False)
    stepper_pin = models.IntegerField(default=0)
    stepper_1 = models.IntegerField(default=0)
    stepper_2 = models.IntegerField(default=0)
    stepper_3 = models.IntegerField(default=0)
    servo_1 = models.IntegerField(default=0)
    servo_2 = models.IntegerField(default=0)
    servo_3 = models.IntegerField(default=0)
    gripper = models.IntegerField(default=0)

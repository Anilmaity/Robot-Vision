import datetime

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Robot


class set_angles(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


    def post(self, request):
        id = request.data['id_no']
        stepper_1 = request.data['stepper_1']
        stepper_2 = request.data['stepper_2']
        stepper_3 = request.data['stepper_3']
        servo_1 = request.data['servo_1']
        servo_2 = request.data['servo_2']
        servo_3 = request.data['servo_3']



        robot = Robot.objects.get(id_no=id)
        robot.stepper_1 = stepper_1
        robot.stepper_2 = stepper_2
        robot.stepper_3 = stepper_3
        robot.servo_1 = servo_1
        robot.servo_2 = servo_2
        robot.servo_3 = servo_3
        robot.save()
        return Response({"message": "Angles update Successfully"})

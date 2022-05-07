import datetime

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Robot


class register_robot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


    def post(self, request):
        id = request.data['id']

        robot = Robot.objects.get(id=id).exists()
        if(robot):
            return Response({"message": "Robot already exists"})

        else:

            robot = Robot.objects.create(
                id=id,
                id_no=id
            )
            robot.save()
            return Response({"message": "Robot added Successfully"})

import datetime

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Robot
from api.serializers import RobotSerializer

class get_angles(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        id = request.data['id_no']
        print(id)

        robot = Robot.objects.get(id_no=id)
        print(robot)
        ser = RobotSerializer(robot)
        print(ser.data)

        return Response(ser.data, status=200)
        #return JsonResponse(ser.data, safe=False)


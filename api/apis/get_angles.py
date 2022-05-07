import datetime

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Robot
from api.serializers import RobotSerializer

class get_angles(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        id = request.data['id_no']

        robot = Robot.objects.get(id_no=id)

        ser = RobotSerializer(robot,many=True)
        return JsonResponse(ser.data, safe=False)


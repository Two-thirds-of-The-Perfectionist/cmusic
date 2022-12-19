from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer


class RegisterUserView(APIView):

    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        ser = RegisterUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response('Successfully registration')

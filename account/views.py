from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer, UserSerializer
from .models import User


class RegisterUserView(APIView):

    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        ser = RegisterUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response('Successfully registration')


@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = None
    user.save()

    return Response("You appreciate this account", status=200)


@api_view(['DELETE'])
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if user.id != request.user.id:
        return Response('You cant delete this user', status=403)

    user.delete()

    return Response("User successfully deleted", status=204)


@api_view(['GET'])
def details_user(request, id):
    user = get_object_or_404(User, id=id)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=200)

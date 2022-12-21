from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer, NewPasswordSerializer
from .models import User
from .utils import send_activation_mail, send_activation_code


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
def delete_user(request, u_id):
    user = get_object_or_404(User, id=u_id)

    if user.id != request.user.id:
        return Response('You cant delete this user', status=403)

    user.delete()

    return Response("User successfully deleted", status=204)


class ForgotPassword(APIView):

    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(user.email, user.activation_code)

        return Response('send_mail' ,status=200)


class ForgotPasswordAccept(APIView):

    def post(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.activation_code = None
        user.is_active = True
        user.save()
        ser = NewPasswordSerializer(data=request.data)

        if ser.is_valid(raise_exception=True):
            ser.save()

            return Response('Your password successfully update', status=200)

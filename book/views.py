from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer, UserSerializer, NewPasswordSerializer, SubscriptionSerializer
from .models import User, Subscription
from .utils import send_activation_mail, send_activation_code


class RegisterUserView(APIView):

    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        ser = RegisterUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response('Successfully registration')


class ForgotPassword(APIView):

    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(user.email, user.activation_code)

        return Response('send_mail' ,status=200)


@api_view(['POST'])
def new_password_post(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.activation_code = None
    ser = NewPasswordSerializer(data=request.data)

    if ser.is_valid(raise_exception=True):
        user.is_active = True
        user.save()
        ser.save()

        return Response('Your password successfully update', status=200)


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


@api_view(['POST'])
def subscribe(request):
    serializer = SubscriptionSerializer(data=request.data)

    if not serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(status=201)


@api_view(['GET'])
def list_subs(request):
    queryset = Subscription.objects.all().order_by('id')
    serializer = SubscriptionSerializer(queryset, many=True)

    return Response(serializer.data, status=200)

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from book.utils import send_activation_mail


User = get_user_model()


@api_view(['GET'])
def google_login(request):
    return Response('Активационная ссылка (для POST запроса): http://localhost:8000/google/activate/', status=200)


@api_view(['POST'])
def google_activate(request):
    print(request.data)
    if not request.data.get('email'):
        raise ValidationError(detail='Field "email" is required')
    
    email = BaseUserManager.normalize_email(request.data.get('email'))
    user = get_object_or_404(User, email=email)
    user.create_activation_code()
    user.save()
    send_activation_mail(user.email, user.activation_code)

    return Response('Mail sent', status=200)

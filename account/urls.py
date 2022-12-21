from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUserView, activate_view, delete_user, ForgotPassword, new_password_post


urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('activate/<str:activation_code>/', activate_view),
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('delete/<int:u_id>/', delete_user),
    path('forgot/', ForgotPassword.as_view()),
    path('accept/<str:activation_code>/', new_password_post),
]

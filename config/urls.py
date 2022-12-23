"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from oauth_app.views import google_login, google_activate


swagger_view = get_schema_view(
    openapi.Info(
        title='CMUSIC API',
        default_version = 'v1',
        description='cmusic API'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', swagger_view.with_ui('swagger', cache_timeout=0)),
    path('account/', include('book.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('google/login/callback/', google_login),
    path('google/activate/', google_activate),
    path('', include('allauth.urls')),
    path('logout/', LogoutView.as_view()),
    path('', include('main.urls')),
    path('', include('review.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

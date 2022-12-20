from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, MusicViewSet
from .models import Playlist

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('music', MusicViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

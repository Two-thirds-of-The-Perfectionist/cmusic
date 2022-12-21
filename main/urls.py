from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, create_music, get_music, delete_music
from .models import Playlist

router = DefaultRouter()
router.register('posts', PostViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('musics/', get_music),
    path('music-create/', create_music),
    path('music-delete/<int:id>/', delete_music),
]

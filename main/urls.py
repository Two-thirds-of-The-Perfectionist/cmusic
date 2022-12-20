from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, MusicViewSet
from .models import Playlist
# from main.views import delete_playlist, create_playlist

router = DefaultRouter()
router.register('posts', PostViewSet)
# router.register('playlist', PlayListViewSet)
router.register('music', MusicViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

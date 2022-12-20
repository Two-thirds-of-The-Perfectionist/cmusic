from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, MusicViewSet 

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('music', MusicViewSet)


urlpatterns = [
    path('', include(router.urls)),
   
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet


router = DefaultRouter()
router.register('comments/', CommentsViewSet)

urlpatterns = [
    path('', include(router.urls))
]

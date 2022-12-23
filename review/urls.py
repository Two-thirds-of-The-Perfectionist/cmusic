from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CommentViewSet, favorites_list
from main.urls import router

comment_router = NestedSimpleRouter(router, 'posts', lookup='post')
comment_router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(comment_router.urls)),
    path('favorites/', favorites_list),
]

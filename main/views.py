from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view

from .serializers import PostSerializer, MusicSerializer
from .models import Post, Music
from .filters import  PostFilter,LikeFilter



class MusicViewSet(ModelViewSet):
    queryset  = Music.objects.all().order_by('id')
    serializer_class = MusicSerializer


class PostViewSet(ModelViewSet):
    queryset  = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]
    filterset_class = PostFilter, LikeFilter
    

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'search']:
            return []
        return [IsAuthenticatedOrReadOnly()]





    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q',openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    @action(['GET'], detail=False)
    def search(self,requests):
        q = requests.query_params.get('q')
        queryset = self.get_queryset()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q))
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializers = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=201)

  
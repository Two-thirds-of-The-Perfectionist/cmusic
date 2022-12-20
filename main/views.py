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
    # filter_backends = [DjangoFilterBackend]
    

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'search']:
            return []
        return [IsAuthenticatedOrReadOnly()]


    # @swagger_auto_schema(manual_parameters=[
    #     openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    #     ])
    # @action(['GET'], detail=False)
    # def search(self, request):
    #     q =request.query_params.get('q')
    #     queryset = self.get_queryset() 
    #     if q:
    #         queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q)) 
    #     pagination = self.paginate_queryset(queryset)
    #     if pagination:
    #         serializer = self.get_serializer(pagination, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(queryset, many=True) 
    #     return Response(serializer.data, status=200)


# @api_view(['GET'])
# def search(request):
#     q = request.query_params.get('q')
#     qs = Post.objects.filter(title__icontains=q)
#     serializer = PostSerializer(qs, many=True)
#     return Response(serializer.data, status=200)


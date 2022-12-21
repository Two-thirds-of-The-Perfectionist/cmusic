from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import PostSerializer, MusicSerializer, PlayListSerializer
from .models import Post, Music, Playlist
from .filters import PostFilter, LikeFilter
from .permissions import IsAuthorOrReadOnly

from review.models import PostLike, PostFavorite


User = get_user_model()


class MusicViewSet(ModelViewSet):
    queryset  = Music.objects.all().order_by('id')
    serializer_class = MusicSerializer


    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly()]


class PostViewSet(ModelViewSet):
    queryset  = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]
    # filterset_class = PostFilter, LikeFilter
    

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q',openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    @action(['GET'], detail=False)
    def search(self,requests):
        q = requests.query_params.get('q')
        queryset = self.get_queryset()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializers = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=201)
    

    @action(['POST'], detail=True)
    def playlist(self, request, pk=None):
        request.data._mutable = True
        request.data.update({'post': pk})
        serializer = PlayListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)


    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        user_id = request.data.get('user')
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, id=pk)

        if PostLike.objects.filter(post_id=post, user_id=user).exists():
            PostLike.objects.filter(post_id=post, user_id=user).delete()
        else:
            PostLike.objects.create(post_id=post, user_id=user)

        return Response(status=201)


    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        user_id = request.data.get('user')
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, id=pk)

        if PostFavorite.objects.filter(post_id=post, user_id=user).exists():
            PostFavorite.objects.filter(post_id=post, user_id=user).delete()
        else:
            PostFavorite.objects.create(post_id=post, user_id=user)

        return Response(status=201)
    




    def get_permissions(self):
        return [IsAuthorOrReadOnly()]

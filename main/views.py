from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
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


@api_view(['GET'])
def get_music(request):
    queryset = Music.objects.all().order_by('id')
    serializer = MusicSerializer(queryset, many=True)

    return Response(serializer.data, status=200)


@api_view(['POST'])
def create_music(request):
    serializer = MusicSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
    
    return Response(status=201)


@api_view(['DELETE'])
def delete_music(request, id):
    music = get_object_or_404(Music, id=id)
    music.delete()

    return Response(status=204)


# class MusicViewSet(ModelViewSet):
#     queryset  = Music.objects.all().order_by('id')
#     serializer_class = MusicSerializer


    # @swagger_auto_schema(manual_parameters=[
    #     openapi.Parameter('q',openapi.IN_QUERY, type=openapi.TYPE_STRING)
    # ])
    # @action(['GET'], detail=False)
    # def search(request):
    #     q = request.query_params.get('q')
    #     qs = Post.objects.filter(body__icontains=q)
    #     serializer = PostSerializer(qs, many=True)

    #     return Response(serializer.data, status=200)


    # @action(['PATCH'], detail=False)
    # def patch(self, request, pk=None):
    #     user_id = request.data.get('user')
    #     user = get_object_or_404(User, id=user_id)
    #     music = get_object_or_404(Music, id=pk)


    # def get_permissions(self):
    #     return [IsAuthenticatedOrReadOnly()]


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


    @action(['PUT'], detail=True)
    def like(self, request, pk=None):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, id=pk)

        if PostLike.objects.filter(post=post, user=user).exists():
            PostLike.objects.filter(post=post, user=user).delete()
        else:
            PostLike.objects.create(post=post, user=user)

        return Response(status=201)


    @action(['PUT'], detail=True)
    def favorite(self, request, pk=None):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, id=pk)

        if PostFavorite.objects.filter(post=post, user=user).exists():
            PostFavorite.objects.filter(post=post, user=user).delete()
        else:
            PostFavorite.objects.create(post=post, user=user)

        return Response(status=201)


    def get_permissions(self):
        return [IsAuthorOrReadOnly()]

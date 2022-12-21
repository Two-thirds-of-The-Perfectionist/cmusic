from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view

from .serializers import PostSerializer, MusicSerializer
from .models import Post, Music
from .filters import PostFilter, LikeFilter
from .permissions import IsAuthorOrReadOnly

from review.models import PostLike, PostFavorite


User = get_user_model()


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
            queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q))
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializers = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=201)
    

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


# class PlayListViewSet(ModelViewSet):
#     queryset  = PlayList.objects.all().order_by('id')
#     serializer_class = PlayListSerializer
#     permission_classes = [IsAdminUser]


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


# def get_permissions(self):
#     return [IsAuthenticatedOrReadOnly()]

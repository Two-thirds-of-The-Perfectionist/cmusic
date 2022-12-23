from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import NotAcceptable
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


    def update(self, request, *args, **kwargs):
        if request.data.get('music'):
            raise NotAcceptable(detail='Field "music" not available for update')

        request.data.update({'music': self.get_object().music})

        return super().update(request, *args, **kwargs)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()

        if q:
            queryset = queryset.filter(Q(author__icontains=q) | Q(title__icontains=q))
        
        pagination = self.paginate_queryset(queryset)

        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=200)


    def get_permissions(self):
        return [IsAuthorOrReadOnly()]


class PostViewSet(ModelViewSet):
    queryset  = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]
    # filterset_class = PostFilter, LikeFilter
    

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        
        pagination = self.paginate_queryset(queryset)

        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=200)


    @action(['POST'], detail=True)
    def playlist(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        # print(post.user)
        # print(request.user)

        if post.user != request.user:
            raise NotAcceptable('Недостаточно прав')

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

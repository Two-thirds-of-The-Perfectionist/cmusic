from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import PostSerializer
from .models import Post
from review.models import PostLike, PostFavorite


class PostViewSet(ModelViewSet):
    queryset  = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]
   


    def get_permissions(self):
        if self.action in ['retrieve', 'list','search']:
            return [] 
        return [IsAdminUser()] 


    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ])
    @action(['GET'], detail=False)
    def search(self, request):
        q =request.query_params.get('q')
        qs = self.get_queryset() 
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q)) 
        pagination = self.paginate_queryset(qs)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True) 
        return Response(serializer.data, status=200)


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

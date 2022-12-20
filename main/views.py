from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import PostSerializer, MusicSerializer
from .models import Post,Music
from .filters import LikeFilter, PostFilter


class PostViewSet(ModelViewSet):
    queryset  = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [LikeFilter,PostFilter]
   

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

# class PlayListViewSet(ModelViewSet):
#     queryset  = PlayList.objects.all().order_by('id')
#     serializer_class = PlayListSerializer
#     permission_classes = [IsAdminUser]


class MusicViewSet(ModelViewSet):
    queryset  = Music.objects.all().order_by('id')
    serializer_class = MusicSerializer
    permission_classes = [IsAdminUser]


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, CommentLike
from .serializers import CommentSerializer


User = get_user_model()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        user_id = request.data.get('user')
        user = get_object_or_404(User, id=user_id)
        comment = get_object_or_404(Comment, id=pk)
        
        if CommentLike.objects.filter(comment_id=comment, user_id=user).exists():
            CommentLike.objects.filter(comment_id=comment, user_id=user).delete()
        else:
            CommentLike.objects.create(comment_id=comment, user_id=user)
        
        return Response(status=201)

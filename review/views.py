from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comments, CommentsLikes
from .serializers import CommentsSerializer


User = get_user_model()


class CommentsViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        user_id = request.data.get('user')
        user = get_object_or_404(User, id=user_id)
        comment = get_object_or_404(Comments, id=pk)
        
        if CommentsLikes.objects.filter(comment_id=comment, user_id=user).exists():
            CommentsLikes.objects.filter(comment_id=comment, user_id=user).delete()
        else:
            CommentsLikes.objects.create(comment_id=comment, user_id=user)
        
        return Response(status=201)

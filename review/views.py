from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable

from .models import Comment, CommentLike
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly

from main.models import Post


User = get_user_model()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])
    

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data.update({'post': self.kwargs['post_pk']})
        print(request.data)

        return super().create(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        if request.data.get('post'):
            raise NotAcceptable(detail='Field "post" not available for update')

        request.data._mutable = True
        request.data.update({'post': self.get_object().post.id})

        return super().update(request, *args, **kwargs)


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
    

    def get_permissions(self):
        return [IsAuthorOrReadOnly()]

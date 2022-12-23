from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotAuthenticated

from .models import Comment, CommentLike, PostFavorite
from .serializers import CommentSerializer, PostFavoriteSerializer
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

        return super().create(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        if request.data.get('post'):
            raise NotAcceptable(detail='Field "post" not available for update')

        request.data._mutable = True
        request.data.update({'post': self.get_object().post.id})

        return super().update(request, *args, **kwargs)


    @action(['PUT'], detail=True)
    def like(self, request, post_pk, pk=None):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        comment = get_object_or_404(Comment, id=pk)

        if CommentLike.objects.filter(comment=comment, user=user).exists():
            CommentLike.objects.filter(comment=comment, user=user).delete()
        else:
            CommentLike.objects.create(comment=comment, user=user)

        return Response(status=201)
    

    def get_permissions(self):
        return [IsAuthorOrReadOnly()]


@api_view(['GET'])
def favorites_list(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated(detail='Authentication required')

    queryset = PostFavorite.objects.filter(user=request.user)
    serializer = PostFavoriteSerializer(queryset, many=True)

    return Response(serializer.data, status=200)

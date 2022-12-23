from rest_framework.serializers import ModelSerializer

from .models import Comment, PostFavorite
from main.serializers import PostSerializer


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)


    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()

        return rep


class PostFavoriteSerializer(ModelSerializer):
    class Meta:
        model = PostFavorite
        fields = ('post',)


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['post'] = PostSerializer(instance.post).data

        return rep

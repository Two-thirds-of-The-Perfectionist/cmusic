from rest_framework.serializers import ModelSerializer
from .models import Post, Playlist, Music


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user',)
    
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        rep['author'] = instance.user.username
        rep['playlist'] = PlayListSerializer(instance.playlist.all(), many=True).data

        return rep


class PlayListSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('post', 'music')


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['music'] = MusicSerializer(instance.music).data

        return rep


class MusicSerializer(ModelSerializer):
    
    class Meta:
        model = Music
        exclude = ('user',)


    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs

from rest_framework.serializers import ModelSerializer
from .models import Post, Playlist, Music

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user_id',)
    
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user_id'] = request.user

        return attrs
    

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['user_id']= instance.user


class PlayListSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'



class MusicSerializer(ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

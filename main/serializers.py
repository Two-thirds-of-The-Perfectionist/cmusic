from rest_framework.serializers import ModelSerializer
from .models import Post, PlayList, Music

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['user_id']= instance.user


class PlayListSerializer(ModelSerializer):
    class Meta:
        model = PlayList
        fields = '__all__'



class MusicSerializer(ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'



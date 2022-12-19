from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all_'

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['user_id']= instance.user

  



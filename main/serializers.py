from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user_id',)
    
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')  # получаем запрос из view
        attrs['user_id'] = request.user

        return attrs
    

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['user_id']= instance.user

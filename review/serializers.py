from rest_framework.serializers import ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user_id',) 


    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user_id'] = request.user

        return attrs

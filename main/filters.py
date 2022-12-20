from django_filters.rest_framework import FilterSet
import django_filters

from review.models import PostLikes
from .models import Post

class LikeFilter(FilterSet):
    like_filter = django_filters.CharFilter(field_name='like_filter')
    
    
    class Meta:
        model = PostLikes        
        fields = ['like_filter']


class PostFilter(FilterSet):
    post_filter = django_filters.DateTimeFilter(field_name='post__filter')


    class Meta:
        model = Post
        fields = ['post_filter']



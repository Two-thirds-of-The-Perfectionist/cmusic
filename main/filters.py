from django_filters.rest_framework import FilterSet
import django_filters

from review.models import PostLike
from .models import Post

class LikeFilter(FilterSet):
    like_filter = django_filters.CharFilter(field_name='like__filter')
    
    
    class Meta:
        model = PostLike        
        fields = ['like_filter']


class PostFilter(FilterSet):
    post_filter = django_filters.DateTimeFilter(field_name='post__filter')


    class Meta:
        model = Post
        fields = ['post_filter']



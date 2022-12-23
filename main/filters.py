from django_filters.rest_framework import FilterSet
import django_filters

from .models import Post
from review.models import PostLike


class PostFilter(FilterSet):
    post_filter = django_filters.DateTimeFilter(field_name='post__filter')


    class Meta:
        model = Post
        fields = ['post_filter']


class LikeFilter(FilterSet):
    like_filter = django_filters.CharFilter(field_name='like__filter')
    
    
    class Meta:
        model = PostLike
        fields = ['like_filter']

from django_filters.rest_framework import FilterSet
import django_filters

from .models import Post


class PostFilter(FilterSet):
    created_at = django_filters.DateTimeFilter(field_name='created_at')


    class Meta:
        model = Post
        fields = ['created_at']

from django.db import models
from django.contrib.auth import get_user_model

from main.models import Post


User = get_user_model()


class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)


class PostLike(models.Model):
    user_id = models.ForeignKey(User, related_name='post_likes' , on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)


class PostFavorite(models.Model):
    user_id = models.ForeignKey(User, related_name='post_favorites' , on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='favorites', on_delete=models.CASCADE)


class CommentLike(models.Model):
    user_id = models.ForeignKey(User, related_name='comment_likes', on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)

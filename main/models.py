from django.db import models
from django.contrib.auth import get_user_model
# from .models import Music

User = get_user_model()

class Post(models.Model):
    user_id = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    cover = models.ImageField(upload_to='post_cover', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.username} -> {self.description}'


class Music(models.Model):
    music = models.FileField(upload_to='music')
    title = models.CharField(max_length=250)
    cover = models.ImageField(upload_to='music_cover')


class Playlist(models.Model):
    post_id = models.ForeignKey(Post, related_name='playlist' ,on_delete=models.CASCADE)
    music_id = models.ForeignKey(Music, related_name='playlist',on_delete=models.CASCADE)

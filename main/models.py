from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    description = models.TextField()
    cover = models.ImageField(upload_to='post_cover', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def average(self):
        posts = Post.objects.filter(updated_at=self)
        values = []
        for post in posts:
            values.append(post.average_rating)
        if values:
            return sum(values) / len(values)
        return 0


class Music(models.Model):
    music = models.FileField(upload_to='music')
    author = models.CharField(max_length=24)
    title = models.CharField(max_length=24)
    cover = models.ImageField(upload_to='music_cover')


class Playlist(models.Model):
    post = models.ForeignKey(Post, related_name='playlist' ,on_delete=models.CASCADE)
    music = models.ForeignKey(Music, related_name='playlist',on_delete=models.CASCADE)

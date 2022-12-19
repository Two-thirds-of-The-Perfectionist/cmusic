from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(models.Model):
    user_id = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    cover = models.ImageField(upload_to='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.author.username} -> {self.body}'


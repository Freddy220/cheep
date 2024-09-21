from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def __str__(self):
        return self.title

#Actualizacion del modelo

    def like_count(self):
        return self.likes.count()

    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists()
    
    
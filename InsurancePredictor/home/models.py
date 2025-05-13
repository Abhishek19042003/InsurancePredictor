from django.db import models
class Post(models.Model):
    banner=models.ImageField(default='xyz.png',blank=True)

    def __str__(self):
        return self.banner
# Create your models here.

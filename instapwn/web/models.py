from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.TextField(max_length=60)
    content = models.TextField(max_length=255)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True)

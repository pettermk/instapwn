from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.TextField(max_length=60)
    content = models.TextField(max_length=255)


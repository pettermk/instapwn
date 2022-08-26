from django.forms import Form
from django import forms

from web.models import Post


class PostForm(Form):
    title = forms.CharField(max_length=60)
    content = forms.CharField(widget=forms.Textarea({'rows': '5'}))
    image = forms.ImageField()

class DeletePostForm(Form):
    class Meta:
        model = Post
        fields = []

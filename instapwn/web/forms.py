from django.forms import Form
from django import forms


class PostForm(Form):
    title = forms.CharField(max_length=60)
    content = forms.CharField(widget=forms.Textarea({'rows': '5'}))

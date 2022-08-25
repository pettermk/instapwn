from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login

from web.forms import PostForm

def index(request):
    return render(request, 'web/index.html', {'PostForm': PostForm()})

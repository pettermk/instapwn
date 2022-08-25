from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login


def index(request):
    return render(request, 'web/index.html')

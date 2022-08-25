from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login

from web.forms import PostForm
from web.models import Post

def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post = Post(
                author = request.user,
                title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            post.save()
    posts = Post.objects.all()
    return render(
        request,
        'web/index.html',
        {
            'PostForm': PostForm(),
            'posts': posts
        }
    )

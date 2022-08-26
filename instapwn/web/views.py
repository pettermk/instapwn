from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.contrib.auth import login

from web.forms import PostForm, DeletePostForm
from web.models import Post

def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            post = Post(
                author = request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                image=form.cleaned_data['image']
            )
            post.save()
    posts = Post.objects.all()
    return render(
        request,
        'web/index.html',
        {
            'PostForm': PostForm(),
            'DeletePostForm': DeletePostForm(),
            'posts': posts
        }
    )

def delete_post(request, pk):
    post_to_delete = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = DeletePostForm(request.POST)
        if form.is_valid():
            post_to_delete.delete()
            return HttpResponseRedirect("/")
    
    return HttpResponseRedirect("/")

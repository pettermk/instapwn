from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/delete/<pk>', views.delete_post, name='delete_post')
]

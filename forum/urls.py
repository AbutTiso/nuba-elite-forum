from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('thread/<slug:slug>/', views.thread_detail, name='thread'),
    path('category/<slug:slug>/create/', views.create_thread, name='create_thread'),
    path('thread/<slug:slug>/reply/', views.reply_thread, name='reply'),
    path('thread/<slug:slug>/like/', views.like_thread, name='like_thread'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]

from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='list'),
    path('<slug:slug>/', views.article_detail, name='detail'),
    path('<slug:slug>/like/', views.like_article, name='like'),
    path('<slug:slug>/edit/', views.edit_article, name='edit'),
    path('<slug:slug>/delete/', views.delete_article, name='delete'),
]

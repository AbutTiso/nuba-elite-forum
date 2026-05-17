from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('my-threads/', views.my_threads, name='my_threads'),
    path('my-posts/', views.my_posts, name='my_posts'),
]

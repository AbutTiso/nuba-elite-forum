from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('join/', views.join, name='join'),
    path('join/success/', views.join_success, name='join_success'),
]

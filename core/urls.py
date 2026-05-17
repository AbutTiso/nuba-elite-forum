from django.urls import path
from . import views
from .search_views import search

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('focus-areas/', views.focus_areas, name='focus_areas'),
    path('search/', search, name='search'),
    path('donate/', views.donate, name='donate'),
]

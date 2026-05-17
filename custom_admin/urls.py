from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('members/', views.members, name='members'),
    path('members/<int:member_id>/approve/', views.approve_member, name='approve_member'),
    path('members/<int:member_id>/suspend/', views.suspend_member, name='suspend_member'),
    path('members/<int:member_id>/make-admin/', views.make_admin, name='make_admin'),
    path('members/<int:member_id>/remove-admin/', views.remove_admin, name='remove_admin'),
    path('articles/', views.articles, name='articles'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/delete/', views.delete_article, name='delete_article'),
    path('events/', views.events, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('messages/', views.messages_view, name='messages'),
    path('subscribers/', views.subscribers, name='subscribers'),
    path('members/<int:member_id>/delete/', views.delete_member, name='delete_member'),
]

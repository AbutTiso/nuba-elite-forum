from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation'),
    path('new/<str:username>/', views.start_conversation, name='start'),
    path('unread/', views.unread_count, name='unread'),
]

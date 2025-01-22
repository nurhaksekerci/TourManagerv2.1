from django.urls import path
from .views import index, room, start_chat, message_list_create_view

urlpatterns = [
    path('', index, name='index'),
    path('room/<str:room_name>/', room, name='room'),
    path('start_chat/<str:username>/', start_chat, name='start_chat'),
    path('api/messages/', message_list_create_view, name='message-list-create'),
]

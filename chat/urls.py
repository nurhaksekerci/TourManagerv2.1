from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="chat"),
    path("<str:room_name>/", views.room, name="room"),
    path("start-chat/<str:username>/", views.start_chat, name="start_chat"),
]
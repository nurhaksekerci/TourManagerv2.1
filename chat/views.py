from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q


def index(request):
    users = User.objects.all().exclude(username = request.user.username)
    
    return render(request, "chat/index.html",{'users' : users})


def room(request, room_name):
    requestUser = User.objects.get(username = request.user.username)
    users = User.objects.all().exclude(username = request.user.username)
    room = Room.objects.get(id = room_name)
    messages = Message.objects.filter(room = room)
    if room.first_user == requestUser : 
        user_full_name = f"{ room.second_user.first_name } { room.second_user.last_name }" 
    else:
        user_full_name = f"{ room.first_user.first_name } { room.first_user.last_name }" 
    return render(request, "chat/roomv2.html", {"room_name": room_name, 'users' : users, 'room' : room, 'user_full_name' : user_full_name, 'messages' : messages})


def start_chat(request, username):
    second_user = User.objects.get(username = username)
    room = Room.objects.filter(
        (Q(first_user=request.user) & Q(second_user=second_user)) | 
        (Q(first_user=second_user) & Q(second_user=request.user))
    ).first()
    
    # Eğer oda yoksa yeni bir oda oluşturun
    if not room:
        room = Room.objects.create(first_user=request.user, second_user=second_user)
    
    return redirect("room", room.id)
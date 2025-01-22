from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Room, Message
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer

def index(request):
    users = User.objects.all().exclude(username=request.user.username)
    return render(request, "chat/index.html", {'users': users})

def room(request, room_name):
    requestUser = User.objects.get(username=request.user.username)
    users = User.objects.all().exclude(username=request.user.username)
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)
    if room.first_user == requestUser:
        user_full_name = f"{room.second_user.first_name} {room.second_user.last_name}"
    else:
        user_full_name = f"{room.first_user.first_name} {room.first_user.last_name}"
    return render(request, "chat/roomv2.html", {
        "room_name": room_name, 
        'users': users, 
        'room': room, 
        'user_full_name': user_full_name, 
        'messages': messages
    })

def start_chat(request, username):
    second_user = User.objects.get(username=username)
    room = Room.objects.filter(
        (Q(first_user=request.user) & Q(second_user=second_user)) | 
        (Q(first_user=second_user) & Q(second_user=request.user))
    ).first()

    if not room:
        room = Room.objects.create(first_user=request.user, second_user=second_user)
    
    return redirect("room", room.id)

@csrf_exempt
@api_view(['GET', 'POST'])
def message_list_create_view(request):
    if request.method == 'GET':
        room_name = request.query_params.get('room_name')
        room = Room.objects.get(id=room_name)
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        room_name = data.get('room')
        room = Room.objects.get(id=room_name)
        user = User.objects.get(username=data.get('user'))
        content = data.get('content')
        message_type = data.get('message_type')
        
        message = Message.objects.create(
            room=room,
            user=user,
            content=content,
            message_type=message_type,
            created_date=timezone.now()
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

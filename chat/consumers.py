import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room
from django.utils import timezone
import pytz

# Türkiye saat dilimini alın
turkey_tz = pytz.timezone('Europe/Istanbul')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json["message_type"]
        user = self.scope["user"]



        # Veritabanına mesaj ekle
        m = await self.create_message(message, user, self.room_name, message_type)
        time = f"{m.created_date.hour}:{m.created_date.minute:02d}"
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "user": user.username, 'created_date' : time, "message_type" : message_type}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        created_date = event["created_date"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user": user, 'created_date' : created_date}))

    @database_sync_to_async
    def create_message(self, message, user, room_name, message_type):
        created_date_utc = timezone.now()
        created_date_turkey = created_date_utc.astimezone(turkey_tz)
        room = Room.objects.get(id=room_name)
        m = Message.objects.create(content=message, user=user, room=room, created_date=created_date_turkey, message_type = message_type)
        return m
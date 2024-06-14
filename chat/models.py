import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    id = models.UUIDField(verbose_name="Oda ID", primary_key=True, default=uuid.uuid4)
    first_user = models.ForeignKey(User, related_name="room_first", verbose_name="Kullanıcı", on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, related_name="room_second", verbose_name="Kullanıcı", on_delete=models.CASCADE)


class Message(models.Model):
    user = models.ForeignKey(User, verbose_name="Gönderen", related_name="messages", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name="Oda", related_name="messages", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Mesaj içeriği")
    created_date = models.DateTimeField(verbose_name="Tarih")
    message_type = models.CharField(verbose_name="Dosya türü", max_length=50, default="message")
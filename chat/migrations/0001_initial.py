# Generated by Django 4.2.11 on 2024-06-09 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Oda ID",
                    ),
                ),
                (
                    "first_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_first",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Kullanıcı",
                    ),
                ),
                (
                    "second_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_second",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Kullanıcı",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="Mesaj içeriği")),
                ("created_date", models.DateTimeField(verbose_name="Tarih")),
                (
                    "message_type",
                    models.CharField(
                        default="message", max_length=50, verbose_name="Dosya türü"
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.room",
                        verbose_name="Oda",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Gönderen",
                    ),
                ),
            ],
        ),
    ]
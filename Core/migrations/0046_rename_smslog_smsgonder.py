# Generated by Django 4.2.11 on 2024-05-27 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0045_smslog"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SmsLog",
            new_name="Smsgonder",
        ),
    ]

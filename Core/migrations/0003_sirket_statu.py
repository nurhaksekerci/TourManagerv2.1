# Generated by Django 4.2.11 on 2024-04-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_personel_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='sirket',
            name='statu',
            field=models.CharField(choices=[('demo', 'Demo'), ('basic', 'Basic'), ('team', 'Team'), ('professional', 'Professional')], default='demo', max_length=20, verbose_name='Statü'),
        ),
    ]

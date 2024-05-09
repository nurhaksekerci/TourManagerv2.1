# Generated by Django 4.2.11 on 2024-05-07 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0025_notification_notificationreceipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.sirket', verbose_name='Sirket'),
        ),
    ]
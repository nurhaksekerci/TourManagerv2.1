# Generated by Django 4.2.11 on 2024-04-28 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0006_activity_activitycost_activitysupplier_buyercompany_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personel',
            name='dark_mode',
            field=models.BooleanField(default=False, verbose_name='Dark Mode'),
        ),
    ]

# Generated by Django 4.2.11 on 2024-04-28 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0008_useractivitylog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitycost',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB (人民币)')], default='TL', max_length=3, verbose_name='Para Birimi'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB (人民币)')], default='TL', max_length=3, verbose_name='Para Birimi'),
        ),
    ]
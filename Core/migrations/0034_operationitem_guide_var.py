# Generated by Django 4.2.11 on 2024-05-09 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0033_remove_operationitemtemplate_day_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationitem',
            name='guide_var',
            field=models.CharField(choices=[('Evet', 'Evet'), ('Hayır', 'Hayır')], default='Hayır', max_length=20, verbose_name='Rehber var mı?'),
        ),
    ]

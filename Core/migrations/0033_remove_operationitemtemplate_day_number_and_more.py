# Generated by Django 4.2.11 on 2024-05-09 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0032_remove_operationdaytemplate_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationitemtemplate',
            name='day_number',
        ),
        migrations.AddField(
            model_name='operationitemtemplate',
            name='day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.operationdaytemplate', verbose_name='Operasyonday Şablonu'),
        ),
    ]

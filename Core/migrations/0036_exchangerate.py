# Generated by Django 4.2.9 on 2024-05-20 10:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0035_alter_museum_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usd_to_try', models.FloatField(verbose_name='USD to TRY')),
                ('usd_to_eur', models.FloatField(verbose_name='USD to EUR')),
                ('usd_to_rmb', models.FloatField(verbose_name='USD to RMB')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Döviz Kuru',
                'verbose_name_plural': 'Döviz Kurları',
            },
        ),
    ]

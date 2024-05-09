# Generated by Django 4.2.11 on 2024-04-25 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sirket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, verbose_name='Adı')),
                ('start', models.DateField(verbose_name='Başlama Tarihi')),
                ('finish', models.DateField(verbose_name='Bitiş Tarihi')),
                ('is_active', models.BooleanField(verbose_name='Aktif mi?')),
            ],
        ),
        migrations.CreateModel(
            name='Personel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif mi?')),
                ('job', models.CharField(choices=[('Satış Personeli', 'Satış Personeli'), ('Operasyon Şefi', 'Operasyon Şefi'), ('Sistem Geliştiricisi', 'Sistem Geliştiricisi'), ('Yönetim', 'Yönetim')], default='Satış Personeli', max_length=20, verbose_name='Görevi')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.sirket', verbose_name='Sirket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personel', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]

# Generated by Django 4.2.11 on 2024-06-13 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0076_cari_guide"),
    ]

    operations = [
        migrations.AddField(
            model_name="cari",
            name="is_delete",
            field=models.BooleanField(default=False, verbose_name="Silindi mi?"),
        ),
    ]
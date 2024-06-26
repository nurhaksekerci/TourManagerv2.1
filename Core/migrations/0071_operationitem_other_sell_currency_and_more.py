# Generated by Django 4.2.11 on 2024-06-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0070_operationitem_activity_sell_currency_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="operationitem",
            name="other_sell_currency",
            field=models.CharField(
                choices=[("TL", "TL"), ("USD", "USD"), ("EUR", "EUR"), ("RMB", "RMB")],
                default="USD",
                max_length=3,
                verbose_name="Diğer Ücretler Para Birimi",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="other_sell_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Diğer Ücretler",
            ),
        ),
    ]

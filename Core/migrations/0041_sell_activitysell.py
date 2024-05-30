# Generated by Django 4.2.11 on 2024-05-25 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0040_operation_is_delete_operationday_is_delete_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sell",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "car",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Maliyet Binek",
                    ),
                ),
                (
                    "minivan",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Maliyet Minivan",
                    ),
                ),
                (
                    "minibus",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Maliyet Minibüs",
                    ),
                ),
                (
                    "midibus",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Maliyet Midibüs",
                    ),
                ),
                (
                    "bus",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Maliyet Otobüs",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("TL", "TL"),
                            ("USD", "USD"),
                            ("EUR", "EUR"),
                            ("RMB", "RMB (人民币)"),
                        ],
                        default="TL",
                        max_length=3,
                        verbose_name="Para Birimi",
                    ),
                ),
                (
                    "is_delete",
                    models.BooleanField(default=False, verbose_name="Silindi mi?"),
                ),
                (
                    "buyer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Core.buyercompany",
                        verbose_name="Firma",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Core.sirket",
                        verbose_name="Sirket",
                    ),
                ),
                (
                    "tour",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Core.tour",
                        verbose_name="Tur",
                    ),
                ),
                (
                    "transfer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Core.transfer",
                        verbose_name="Transfer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Activitysell",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Ücreti",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("TL", "TL"),
                            ("USD", "USD"),
                            ("EUR", "EUR"),
                            ("RMB", "RMB (人民币)"),
                        ],
                        default="TL",
                        max_length=3,
                        verbose_name="Para Birimi",
                    ),
                ),
                (
                    "is_delete",
                    models.BooleanField(default=False, verbose_name="Silindi mi?"),
                ),
                (
                    "activity",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Core.activity",
                        verbose_name="Activite",
                    ),
                ),
                (
                    "buyer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Core.buyercompany",
                        verbose_name="Firma",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Core.sirket",
                        verbose_name="Sirket",
                    ),
                ),
            ],
        ),
    ]

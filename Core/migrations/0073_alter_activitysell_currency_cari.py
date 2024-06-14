# Generated by Django 4.2.11 on 2024-06-12 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0072_alter_operationitem_other_currency_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activitysell",
            name="currency",
            field=models.CharField(
                choices=[("TL", "TL"), ("USD", "USD"), ("EUR", "EUR"), ("RMB", "RMB")],
                default="TL",
                max_length=3,
                verbose_name="Para Birimi",
            ),
        ),
        migrations.CreateModel(
            name="Cari",
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
                    "transaction_type",
                    models.CharField(
                        choices=[("income", "Gelir"), ("expense", "Gider")],
                        max_length=7,
                    ),
                ),
                (
                    "income",
                    models.CharField(
                        blank=True,
                        choices=[("Truzim", "Truzim")],
                        max_length=30,
                        null=True,
                        verbose_name="Gelir Kaynağı",
                    ),
                ),
                (
                    "expense",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Arac", "Araç Ödemesi"),
                            ("Aktivite", "Aktivite Ödemesi"),
                            ("Rehber", "Rehber Ödemesi"),
                            ("Otel", "Otel Ödemesi"),
                            ("Müze", "Müze Ödemeleri"),
                            ("Maas", "Maaş Ödemesi"),
                            ("Fatura", "Fatura Ödemeleri"),
                            ("Vergi", "Vergi Ödemeleri"),
                            ("Diğer", "Diğer Ödemeler"),
                        ],
                        max_length=30,
                        null=True,
                        verbose_name="Gider Kaynağı",
                    ),
                ),
                (
                    "receipt",
                    models.FileField(blank=True, null=True, upload_to="receipts/"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10, verbose_name="Tutar"
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("TL", "TL"),
                            ("USD", "USD"),
                            ("EUR", "EUR"),
                            ("RMB", "RMB"),
                        ],
                        default="TL",
                        max_length=3,
                        verbose_name="Para Birimi",
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
                    ),
                ),
                (
                    "update_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Güncelleme Tarihi"
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
                    "created_staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="olusturan",
                        to="Core.personel",
                        verbose_name="Oluşturan Personel",
                    ),
                ),
            ],
        ),
    ]

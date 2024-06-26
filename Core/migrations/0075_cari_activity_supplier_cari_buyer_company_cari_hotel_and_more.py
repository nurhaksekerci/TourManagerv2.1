# Generated by Django 4.2.11 on 2024-06-12 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0074_cari_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="cari",
            name="activity_supplier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="aktivite_gider",
                to="Core.activitysupplier",
                verbose_name="Aktivite Tedarikçisi",
            ),
        ),
        migrations.AddField(
            model_name="cari",
            name="buyer_company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="gelir_firma",
                to="Core.buyercompany",
                verbose_name="Firmalar",
            ),
        ),
        migrations.AddField(
            model_name="cari",
            name="hotel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="otel_gider",
                to="Core.hotel",
                verbose_name="Oteller",
            ),
        ),
        migrations.AddField(
            model_name="cari",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="arac_gider",
                to="Core.supplier",
                verbose_name="Araç Tedarikçisi",
            ),
        ),
    ]

# Generated by Django 4.2.11 on 2024-05-06 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0016_alter_operationitem_activity_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationitem',
            name='activity_cost',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.activitycost', verbose_name='Aktivite Maliyet'),
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('login_issue', 'Giriş Sorunu'), ('payment_issue', 'Ödeme Sorunu'), ('bug_report', 'Hata Bildirimi'), ('account_info', 'Hesap Bilgisi Sorgulama'), ('suggestion', 'Öneri'), ('training', 'Eğitim')], default='login_issue', max_length=100, verbose_name='Başlık')),
                ('description', models.TextField(verbose_name='Açıklama')),
                ('status', models.CharField(choices=[('open', 'Açık'), ('in_progress', 'İşlemde'), ('closed', 'Kapalı')], default='open', max_length=20, verbose_name='Durum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Zamanı')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Zamanı')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.sirket', verbose_name='Sirket')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.personel', verbose_name='Kaydı Açan')),
            ],
            options={
                'verbose_name': 'Destek Kaydı',
                'verbose_name_plural': 'Destek Kayıtları',
            },
        ),
    ]

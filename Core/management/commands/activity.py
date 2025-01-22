import json
from django.core.management.base import BaseCommand
from Core.models import *
from datetime import datetime


class Command(BaseCommand):
    help = 'İtem modelindeki tüm verileri JSON olarak kaydeder.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=f'companies_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            help='Kaydedilecek JSON dosyasının adı'
        )

    def handle(self, *args, **kwargs):
        output_file = kwargs['output']

        items = Buyercompany.objects.filter(is_delete=False)

        # Verileri JSON formatına dönüştür
        data = []
        for item in items:
            data.append({
                'id': item.id,
                'name': item.name,
                'short_name': item.short_name,
                'contact': item.contact,
            })

        # JSON dosyasını kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Tüm veriler başarıyla "{output_file}" dosyasına kaydedildi.'))

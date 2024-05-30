from django.core.management.base import BaseCommand
from Core.models import *

class Command(BaseCommand):
    help = 'My custom Django command'

    tours = Supplier.objects.filter(company__id=2)

    def handle(self, *args, **options):
        # Türkçe karakterleri İngilizce karakterlere dönüştürmek için bir sözlük oluşturun
        turkish_to_english = {
            'İ': 'I', 'ı': 'i',
            'Ö': 'O', 'ö': 'o',
            'Ü': 'U', 'ü': 'u',
            'Ğ': 'G', 'ğ': 'g',
            'Ş': 'S', 'ş': 's',
            'Ç': 'C', 'ç': 'c'
        }

        for tour in self.tours:
            # Türkçe karakterleri İngilizce karakterlere dönüştürün
            for turkish_char, english_char in turkish_to_english.items():
                tour.name = tour.name.replace(turkish_char, english_char)


            # Tur adını büyük harfe çevirin
            tour.name = tour.name.upper()

            tour.save()

        self.stdout.write(self.style.SUCCESS('Successfully executed my custom command!'))

from django.core.management.base import BaseCommand
from Core.models import Hotel

class Command(BaseCommand):
    help = 'Tekrarlı kayıtları silme, sadece bir tane bırak'

    def handle(self, *args, **options):
        hotels = Hotel.objects.filter(company__id=2).order_by('name', 'city')
        seen = {}

        for hotel in hotels:
            key = (hotel.name, hotel.city)
            if key in seen:
                hotel.delete()
            else:
                seen[key] = hotel

from django.core.management.base import BaseCommand
from Core.models import Operationitem


class Command(BaseCommand):
    """
    Aktivite Fiyat hesaplama komutu
    """

    help = "Şirket ID'si 2 olan ve silinmemiş aktivite kayıtlarını manuel_activity_price alanına günceller."

    def handle(self, *args, **options):
        """
        Aktivite Fiyatlarını manuel_activity_price alanına günceller.
        """

        items = Operationitem.objects.filter(
            activity_price__isnull=False
        ).exclude(activity_price=0)  # Exclude items with activity_price of 0

        for item in items:
            activity_price = item.activity_price
            try:
                item.manuel_activity_price = activity_price
                item.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Item {item.id} için aktivite fiyatı güncellendi.")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Hata: Item {item.id} için aktivite fiyatı güncellenemedi: {e}")
                )
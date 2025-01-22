from django.core.management.base import BaseCommand
from Core.models import UserActivityLog  # Modelinizi doğru şekilde içe aktarın


class Command(BaseCommand):
    help = 'Action alanında "Tour oluşturdu. ID:" geçen tüm kayıtları konsola yazdırır.'

    def handle(self, *args, **kwargs):
        try:
            # "Tour oluşturdu. ID:" içeren kayıtları filtrele
            logs = UserActivityLog.objects.filter(action__icontains="Activity oluşturdu. ID:")

            if not logs.exists():
                self.stdout.write(self.style.WARNING("Hiçbir kayıt bulunamadı."))
                return

            # Kayıtları konsola yazdır
            self.stdout.write(self.style.SUCCESS("Aşağıdaki kayıtlar bulundu:"))
            for log in logs:
                self.stdout.write(f"{log.timestamp} - {log.staff} - {log.action}")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Bir hata oluştu: {e}"))

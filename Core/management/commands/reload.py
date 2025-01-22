from django.core.management.base import BaseCommand
from Core.models import Operation, Operationday, Operationitem   # Operation modelinizi doğru şekilde import ettiğinizden emin olun

class Command(BaseCommand):
    help = 'Finds and prints the Operation with ticket number'

    def handle(self, *args, **kwargs):
        try:
            # Operation modelinde ticket'ı 1234 olan operasyonu buluyoruz
            operation = Operation.objects.get(ticket='LT010924001Silindi')
            days = Operationday.objects.filter(operation=operation, is_delete=True)
            for day in days:
                day.is_delete = False
                day.save()
                items = Operationitem.objects.filter(day=day, is_delete=True)
                for item in items:
                    item.is_delete = False
                    item.save()
            
            self.stdout.write(self.style.SUCCESS(f'Operation found: {operation}'))
        except Operation.DoesNotExist:
            self.stdout.write(self.style.ERROR('Operation with ticket does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))

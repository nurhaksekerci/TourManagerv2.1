from django.core.management.base import BaseCommand
from decimal import Decimal
from Core.models import Operation, ExchangeRate
import pandas as pd

class Command(BaseCommand):
    help = 'Yalnızca satış fiyatlarını ve USD karşılığını yazdırır ve excele kaydeder.'

    def handle(self, *args, **options):
        operations = Operation.objects.filter(company__id=2, finish__month=7, is_delete=False).order_by('finish')
        data = []

        for operation in operations:
            finish = operation.finish
            exchange = ExchangeRate.objects.filter(created_at__gte=finish).order_by('created_at').first()
            if exchange:
                eur_sales_price = Decimal(operation.eur_sales_price or 0)
                tl_sales_price = Decimal(operation.tl_sales_price or 0)
                rbm_sales_price = Decimal(operation.rbm_sales_price or 0)
                usd_sales_price = Decimal(operation.usd_sales_price or 0)

                usd_to_eur = Decimal(exchange.usd_to_eur)
                usd_to_try = Decimal(exchange.usd_to_try)
                usd_to_rmb = Decimal(exchange.usd_to_rmb)

                total_sales_price = (eur_sales_price / usd_to_eur) + (tl_sales_price / usd_to_try) + (rbm_sales_price / usd_to_rmb) + usd_sales_price
                
                # Toplam satış fiyatını iki ondalık basamakla yuvarla
                total_sales_price = round(total_sales_price, 2)
                
                operation.total_sales_price = total_sales_price
                operation.save()

                data.append({
                    'Ticket': operation.ticket,
                    'Finish': finish,
                    'USD': usd_sales_price,
                    'EUR': eur_sales_price,
                    'TRY': tl_sales_price,
                    'RMB': rbm_sales_price,
                    'USD Equivalent': total_sales_price,
                })
            else:
                self.stdout.write(f"Operation ID: {operation.id}")
                self.stdout.write("Exchange rate information is not available for this operation.\n")

        # Verileri DataFrame'e çevirme ve Excel'e kaydetme
        df = pd.DataFrame(data)
        df.to_excel('operations_sales_7.xlsx', index=False)
        
        self.stdout.write(self.style.SUCCESS('Successfully executed the command and saved to Excel!'))

from django.contrib import admin
from .models import *

class SirketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class PersonelAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name']

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

admin.site.register(Sirket, SirketAdmin)
admin.site.register(Personel, PersonelAdmin)
admin.site.register(UserActivityLog)
admin.site.register(Operation)
admin.site.register(OperationTemplate)
admin.site.register(OperationitemTemplate)
admin.site.register(Cari)
admin.site.register(Operationday)
admin.site.register(OperationdayTemplate)
admin.site.register(Operationitem)
admin.site.register(Vehicle)
admin.site.register(NotificationReceipt)
admin.site.register(Notification)
admin.site.register(ExchangeRate)
admin.site.register(SupportTicket)
admin.site.register(Transfer)
admin.site.register(Hotel)
admin.site.register(Supplier)
admin.site.register(VehiclesupplierCities)
admin.site.register(ActivitysupplierCities)
admin.site.register(Smsgonder)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Buyercompany)
admin.site.register(Konum)
admin.site.register(Tour)
admin.site.register(TourRoute)
admin.site.register(Guide)
admin.site.register(Cost)


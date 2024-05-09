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
admin.site.register(Operationday)
admin.site.register(OperationdayTemplate)
admin.site.register(Operationitem)
admin.site.register(Vehicle)
admin.site.register(NotificationReceipt)
admin.site.register(Notification)

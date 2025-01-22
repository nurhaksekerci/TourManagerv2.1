from django.contrib import admin
from .models import SecurityLog, Maintenance, SiteSettings, SupportTicket, SupportTicketResponse

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('maintenance_mode',)
    actions = ['enable_maintenance_mode', 'disable_maintenance_mode']

    def enable_maintenance_mode(self, request, queryset):
        queryset.update(maintenance_mode=True)
        self.message_user(request, "Bakım modu etkinleştirildi.")
    
    def disable_maintenance_mode(self, request, queryset):
        queryset.update(maintenance_mode=False)
        self.message_user(request, "Bakım modu devre dışı bırakıldı.")

    enable_maintenance_mode.short_description = "Bakım Modunu Etkinleştir"
    disable_maintenance_mode.short_description = "Bakım Modunu Devre Dışı Bırak"

class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'event_description', 'ip_address', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('user__username', 'event_description', 'ip_address')

    def has_add_permission(self, request):
        # Loglar sadece sistem tarafından eklenmeli, yönetici panelinden ekleme yapılamaz
        return False

    def has_delete_permission(self, request, obj=None):
        # Loglar silinmemeli, bu yüzden silme izni verilmez
        return False

admin.site.register(SecurityLog, SecurityLogAdmin)
@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('phone', 'created_at')
    search_fields = ('phone',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)



class SupportTicketResponseInline(admin.TabularInline):
    model = SupportTicketResponse
    extra = 1  # Yeni bir cevap eklemek için boş bir form sağlar.
    readonly_fields = ('user', 'created_at')  # Cevabı kimin eklediğini ve ne zaman eklediğini sadece okunabilir yapar.

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'created_at', 'updated_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SupportTicketResponseInline]  # Destek kaydı altında cevapları görüntüler.
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(SupportTicketResponse)
class SupportTicketResponseAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('ticket__title', 'response', 'user__username')
    readonly_fields = ('ticket', 'user', 'created_at')

    def has_add_permission(self, request, obj=None):
        """Cevaplar SupportTicket admin üzerinden eklendiği için ayrı ekleme iznini kapatıyoruz."""
        return False

    def has_change_permission(self, request, obj=None):
        """Cevaplar SupportTicket admin üzerinden değiştirildiği için ayrı değiştirme iznini kapatıyoruz."""
        return False
from django.shortcuts import render
from django.urls import resolve
from .models import SiteSettings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bakım modunu kontrol et
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.maintenance_mode:
            # Kullanıcı yetkisini kontrol et
            try:
                employee = request.user.personel.first()
                if employee and employee.job != 'System Developer':
                    # Admin paneline erişim izni ver
                    if request.path.startswith('/admin/'):
                        return self.get_response(request)
                    # Eğer istek POST ise ve hedef URL 'auth_maintenance' değilse
                    if request.method == 'POST' and resolve(request.path_info).url_name != 'auth_maintenance':
                        return render(request, 'maintenance.html')
                    # Eğer istek GET ise ve herhangi bir sayfa açılmak isteniyorsa
                    if request.method == 'GET':
                        return render(request, 'maintenance.html')
            except AttributeError:
                if request.path.startswith('/admin/'):
                        return self.get_response(request)
                else:
                    return render(request, 'maintenance.html')
        
        # Eğer bakım modu aktif değilse veya kullanıcı yetkiliyse normal akışa devam et
        response = self.get_response(request)
        return response

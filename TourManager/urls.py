"""
URL configuration for TourManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Login.views import *
from Core.views import check_username


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Login.urls')),
    path('', login, name="login"),
    path('daphne/', include('Daphne.urls')),
    path('TourManagerV2/', include('Core.urls')),
    path('tour-app/', include('TourApp.urls')),
    path('auth/', include('LoginApp.urls')),
    path('check_username/', check_username, name='check_username'),
    path('api/', include('api.urls')),

]
from django.conf import settings
from django.conf.urls.static import static

# existing urlpatterns...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


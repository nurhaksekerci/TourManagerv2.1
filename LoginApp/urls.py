from django.urls import path
from . import views

urlpatterns = [
    # Maintenance
    path('maintenance/', views.maintenance, name="auth_maintenance"),

    # User Authentication
    path('login/', views.login_view, name='auth_login'),
    path('logout/', views.logout_view, name='auth_logout'),
    path('register/', views.register_view, name='auth_register'),

    # Password Management
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verify_reset_code/<int:user_id>/', views.verify_reset_code, name='verify_reset_code'),
    path('reset_password_done/<int:user_id>', views.reset_password_done, name='reset_password_done'),
    path('change_password/', views.change_password_view, name='change_password'),

    # Company Views
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),

    # Personnel Views
    path('add_personnel/', views.add_personnel_view, name='add_personnel'),
    path('personnel_list/', views.personnel_list_view, name='personnel_list'),
    path('edit_personnel/<int:id>/', views.edit_personnel_view, name='edit_personnel'),
    path('delete_personnel/<int:id>/', views.delete_personnel_view, name='delete_personnel'),

    # User Profile
    path('profile/', views.profile_view, name='auth_profile'),
    path('profile/<slug:slug>', views.profile_view, name='auth_profile_slug'),

    # Security Logs & Notifications Views
    path('security_logs/', views.security_logs, name='auth_security_logs'),
    path('notifications/', views.notifications, name='auth_notifications'),
    path('support/', views.support, name='auth_support'),
]

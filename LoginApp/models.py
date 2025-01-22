from django.db import models
from django.contrib.auth.models import User

class SiteSettings(models.Model):
    maintenance_mode = models.BooleanField(default=False, verbose_name="Sistem Bakımda mı?")
    
    def __str__(self):
        return f"Bakım Modu: {'Aktif' if self.maintenance_mode else 'Pasif'}"

class Maintenance(models.Model):
    phone = models.CharField(verbose_name=("phone"), max_length=128)
    created_at = models.DateField(verbose_name="Oluşturulma Tarihi", auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.phone

class SecurityLog(models.Model):
    EVENT_CHOICES = [
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_FAILURE', 'Login Failure'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('ACCOUNT_LOCKED', 'Account Locked'),
        ('LOGOUT', 'Logout'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    event_description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    browser_info = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_event_type_display()} - {self.user.username if self.user else "Unknown User"} - {self.timestamp}'


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class SupportTicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response by {self.user.username} on {self.ticket.title}"
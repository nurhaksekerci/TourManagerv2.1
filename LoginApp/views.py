from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Core.models import *
from .models import *
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.cache import cache
import random
import requests
import re
from django.db.models import Q


def maintenance(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        Maintenance.objects.create(phone=phone)
        messages.success(request, 'We will notify you when the maintenance is over.')
        return render(request, 'maintenance.html')
    return render(request, 'maintenance.html')

def log_security_event(user=None, event_type='', event_description='', ip_address=None, browser_info=None):
    SecurityLog.objects.create(
        user=user,
        event_type=event_type,
        event_description=event_description,
        ip_address=ip_address,
        browser_info=browser_info
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', '')

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            log_security_event(
                user=user,
                event_type='LOGIN_SUCCESS',
                event_description='User logged in successfully',
                ip_address=ip_address,
                browser_info=browser_info
            )
            next_url = request.GET.get('next', 'auth_profile')  # next parametresini al, yoksa auth_profile'e yönlendir
            return redirect(next_url)
        else:
            log_security_event(
                event_type='LOGIN_FAILURE',
                event_description=f'Failed login attempt for username: {username}',
                ip_address=ip_address,
                browser_info=browser_info
            )
            messages.error(request, "Invalid username or password.")

    return render(request, 'auth/login.html')
def logout_view(request):
    ip_address = request.META.get('REMOTE_ADDR')
    user = request.user
    browser_info = request.META.get('HTTP_USER_AGENT', '')

    # Kullanıcı çıkış işlemi
    logout(request)
    messages.success(request, "Successfully logged out.")

    # Çıkış olayını kaydet
    log_security_event(
        user=user,
        event_type='LOGOUT',
        event_description='User logged out',
        ip_address=ip_address,
        browser_info=browser_info
    )

    return redirect('auth_login')


def register_view(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', '')

        if password != repassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auth/register.html')

        try:
            start = datetime.date.today()
            finish = start + datetime.timedelta(days=30)

            if company_name:
                company = Company.objects.create(name=company_name, start=start, finish=finish, statu="demo")

                user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
                Personel.objects.create(user=user, company=company, phone=phone, job="Management")

                # Olayı kaydet: Başarılı kayıt
                log_security_event(
                    user=user,
                    event_type='REGISTER_SUCCESS',
                    event_description=f'Registration successful for company: {company_name}',
                    ip_address=ip_address,
                    browser_info=browser_info
                )

                messages.success(request, "Registration successful. Please log in.")
                return redirect('auth_login')
        except Exception as e:
            # Olayı kaydet: Kayıt hatası
            log_security_event(
                event_type='REGISTER_FAILURE',
                event_description=f'Registration failed for email: {email}. Error: {str(e)}',
                ip_address=ip_address,
                browser_info=browser_info
            )

            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'auth/register.html')

    return render(request, 'auth/register.html')

def reset_password(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', '')

        try:
            employee = Personel.objects.get(phone=phone, is_active=True, is_delete=False)
            user = employee.user
        except Employee.DoesNotExist:
            messages.error(request, 'No active user is associated with this phone number.')

            # Kayıt: Kullanıcı bulunamadı
            log_security_event(
                event_type='RESET_PASSWORD_FAILURE',
                event_description=f'Password reset failed. No active user with phone: {phone}',
                ip_address=ip_address,
                browser_info=browser_info
            )
            return redirect('reset_password')

        # Rastgele bir doğrulama kodu oluştur
        verification_code = random.randint(100000, 999999)
        # Kodu cache'de sakla (veya başka bir yöntemle)
        cache.set(f'password_reset_{user.pk}', verification_code, 300)  # 5 dakika geçerli

        # Mesaj içeriğini hazırlayın
        mesaj = f"Your password reset code is: {verification_code}"
        # SOAP servisi kullanarak SMS gönder
        url = "http://soap.netgsm.com.tr:8080/Sms_webservis/SMS?wsdl"
        headers = {'content-type': 'text/xml'}
        body = f"""<?xml version="1.0"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <SOAP-ENV:Body>
                    <ns3:smsGonder1NV2 xmlns:ns3="http://sms/">
                        <username>8503081334</username>
                        <password>6D18AD8</password>
                        <header>MNC GROUP</header>
                        <msg>{mesaj}</msg>
                        <gsm>{phone}</gsm>
                        <encoding>TR</encoding>
                        <filter>0</filter>
                        <startdate></startdate>
                        <stopdate></stopdate>
                    </ns3:smsGonder1NV2>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""

        response = requests.post(url, data=body, headers=headers)

        if response.status_code == 200:
            messages.success(request, 'An SMS with the verification code has been sent.')

            # Kayıt: SMS gönderimi başarılı
            log_security_event(
                user=user,
                event_type='RESET_PASSWORD_SMS_SENT',
                event_description='Password reset SMS sent successfully',
                ip_address=ip_address,
                browser_info=browser_info
            )
            # Kullanıcıyı doğrulama kodu ve yeni şifreyi gireceği sayfaya yönlendir
            return redirect('verify_reset_code', user_id=user.pk)
        else:
            messages.error(request, 'There was an error sending the SMS. Please try again.')

            # Kayıt: SMS gönderimi başarısız
            log_security_event(
                user=user,
                event_type='RESET_PASSWORD_SMS_FAILURE',
                event_description='Failed to send password reset SMS',
                ip_address=ip_address,
                browser_info=browser_info
            )
            return redirect('reset_password')

    return render(request, 'auth/reset_password.html')

def verify_reset_code(request, user_id):
    if request.method == 'POST':
        verification_code = (
            request.POST.get('first') +
            request.POST.get('second') +
            request.POST.get('third') +
            request.POST.get('fourth') +
            request.POST.get('fifth') +
            request.POST.get('sixth')
        )
        # Cache'den doğrulama kodunu al
        cached_code = cache.get(f'password_reset_{user_id}')
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', '')
        user = User.objects.get(pk=user_id)

        if cached_code and str(cached_code) == verification_code:
            # Olayı kaydet: Başarılı doğrulama kodu
            log_security_event(
                user=user,
                event_type='VERIFY_CODE_SUCCESS',
                event_description='Verification code successfully verified',
                ip_address=ip_address,
                browser_info=browser_info
            )
            return redirect('reset_password_done', user_id=user_id)
        else:
            if cached_code is None:
                messages.error(request, 'The verification code has expired. Please request a new one.')
                # Olayı kaydet: Doğrulama kodu süresi doldu
                log_security_event(
                    user=user,
                    event_type='VERIFY_CODE_EXPIRED',
                    event_description='Verification code expired',
                    ip_address=ip_address,
                    browser_info=browser_info
                )
            else:
                messages.error(request, 'Invalid verification code. Please check the code and try again.')
                # Olayı kaydet: Geçersiz doğrulama kodu
                log_security_event(
                    user=user,
                    event_type='VERIFY_CODE_FAILURE',
                    event_description='Invalid verification code attempted',
                    ip_address=ip_address,
                    browser_info=browser_info
                )
            return redirect('verify_reset_code', user_id=user_id)

    return render(request, 'auth/verify_reset_code.html', {'user_id': user_id})

def reset_password_done(request, user_id):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        new_password_confirm = request.POST.get('repassword')
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', '')

        if new_password != new_password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password_done', user_id=user_id)

        try:
            user = User.objects.get(pk=user_id)
            user.set_password(new_password)
            user.save()

            # Olayı kaydet: Başarılı parola sıfırlama
            log_security_event(
                user=user,
                event_type='PASSWORD_RESET_SUCCESS',
                event_description='Password reset successfully',
                ip_address=ip_address,
                browser_info=browser_info
            )

            messages.success(request, 'Your password has been successfully reset.')
            return redirect('auth_login')
        except User.DoesNotExist:
            # Olayı kaydet: Geçersiz kullanıcı
            log_security_event(
                event_type='PASSWORD_RESET_FAILURE',
                event_description=f'Password reset failed. Invalid user ID: {user_id}',
                ip_address=ip_address,
                browser_info=browser_info
            )

            messages.error(request, 'Invalid user.')
            return redirect('reset_password')

    return render(request, 'auth/reset_password_done.html', {'user_id': user_id})

@login_required(login_url='auth_login')
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('password')
        new_password_confirm = request.POST.get('repassword')
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', '')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
            # Olayı kaydet: Hatalı eski parola
            log_security_event(
                user=request.user,
                event_type='PASSWORD_CHANGE_FAILURE',
                event_description='Incorrect old password provided',
                ip_address=ip_address,
                browser_info=browser_info
            )
            return redirect('change_password')

        if new_password != new_password_confirm:
            messages.error(request, 'New passwords do not match')
            # Olayı kaydet: Yeni parolalar eşleşmiyor
            log_security_event(
                user=request.user,
                event_type='PASSWORD_CHANGE_FAILURE',
                event_description='New passwords do not match',
                ip_address=ip_address,
                browser_info=browser_info
            )
            return redirect('change_password')

        try:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Kullanıcının oturumunu geçersiz kılmamak için

            # Olayı kaydet: Başarılı parola değişikliği
            log_security_event(
                user=request.user,
                event_type='PASSWORD_CHANGE_SUCCESS',
                event_description='Password changed successfully',
                ip_address=ip_address,
                browser_info=browser_info
            )

            messages.success(request, 'Your password has been successfully reset.')
            return redirect('auth_login')
        except Exception as e:
            messages.error(request, 'Your password could not be changed. Please try again.')
            # Olayı kaydet: Parola değişikliği başarısız
            log_security_event(
                user=request.user,
                event_type='PASSWORD_CHANGE_FAILURE',
                event_description=f'Error changing password: {str(e)}',
                ip_address=ip_address,
                browser_info=browser_info
            )
            return redirect('change_password')

    return render(request, 'auth/change_password.html')

@login_required(login_url='auth_login')
def company_dashboard(request):
    return render(request, 'company/company_dashboard.html')

@login_required(login_url='auth_login')
def add_personnel_view(request):
    return render(request, 'personnel/add_personnel.html')

@login_required(login_url='auth_login')
def personnel_list_view(request):
    return render(request, 'personnel/personnel_list.html')

@login_required(login_url='auth_login')
def edit_personnel_view(request, id):
    return render(request, 'personnel/edit_personnel.html')

@login_required(login_url='auth_login')
def delete_personnel_view(request, id):

    return render(request, 'personnel/delete_personnel.html')


def exact_username_filter(logs, username):
    exact_logs = []
    pattern = rf"\busername: {re.escape(username)}\b"
    for log in logs:
        if re.search(pattern, log.event_description):
            exact_logs.append(log)
    return exact_logs

@login_required(login_url='auth_login')
def profile_view(request, slug=None):
    if slug:
        employee = Personel.objects.get(slug=slug)
        slug=True
    else:
        employee = Personel.objects.get(user=request.user)
        slug=False
    plans = Plan.objects.all()
    security_logs = SecurityLog.objects.filter(user=request.user)
    security_logs_with_username = SecurityLog.objects.filter(event_description__icontains=f'username: {request.user.username}')
    exact_security_logs_with_username = exact_username_filter(security_logs_with_username, request.user.username)

    context = {
        'employee': employee,
        'security_logs': security_logs,
        'security_logs_not': exact_security_logs_with_username,
        'plans': plans,
        'company_name': employee.company.name.upper(),
        'title': "Profile",
        'slug' : slug
    }
    return render(request, 'profile/profile.html', context)

# Security Logs & Notifications Views

@login_required(login_url='auth_login')
def security_logs(request):
    return render(request, 'security/security_logs.html')

@login_required(login_url='auth_login')
def notifications(request):
    return render(request, 'notifications/notifications.html')


def support(request):
    user = request.user
    employee = Personel.objects.get(user=user)
    supports = SupportTicket.objects.filter(user=user)
    context = {
        'employee': employee,
        'security_logs': security_logs,
        'company_name': employee.company.name.upper(),
        'title': "Support",
        'supports': supports
    }
    return render(request, 'supports/supports.html', context)
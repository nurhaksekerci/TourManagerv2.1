from django.shortcuts import render
from datetime import datetime, timedelta, date, time
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Core.models import *
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        requestPersonel=Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        try:
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Giriş Yaptı.")
        except Personel.DoesNotExist:
            pass
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Kullanıcının bağlı olduğu şirketi bul
            try:
                personel = Personel.objects.get(user=user)
                company = personel.company
            except Personel.DoesNotExist:
                return render(request, 'login/login.html', {'error': 'Kullanıcı geçerli bir personel değil.'})

            # Şirketin bitiş tarihi kontrolü
            if company.finish >= datetime.today().date():
                # Şirketin bitiş tarihi bugün veya ilerideyse, kullanıcıya giriş izni ver
                user_login(request, user)
                requestPersonel = Personel.objects.get(user = user)
                sirket = requestPersonel.company
                try:
                    UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Giriş Yaptı.")
                except Personel.DoesNotExist:
                    pass
                return redirect('index')  # Giriş başarılı
            else:
                # Şirketin bitiş tarihi geçmişse, şirketi ve tüm personelleri pasifleştir
                company.is_active = False
                company.save()
                Personel.objects.filter(company=company).update(is_active=True)
                user_login(request, user)
                return render(request, 'login/pricing.html', {'error': 'Bu şirketin erişim süresi dolmuştur ve şirket pasifleştirilmiştir. Devam etmek için satın alın!'})
        else:
            return render(request, 'login/login.html', {'error': 'Kullanıcıadı veya Parola Hatalı'})
    else:
        return render(request, 'login/login.html', {'welcome': 'Hoşgeldiniz.'})
def register(request):
    if request.method == 'POST':
        date = datetime.today()
        finish = date + timedelta(7)
        company = request.POST['company']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
        repassword = request.POST['repassword']
        phone = request.POST['phone']

        if password == repassword:
            user = User.objects.create_user(username=username, email=mail, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            create_company = Sirket.objects.create(name=company, start=date, finish=finish, is_active=True)
            personel = Personel.objects.create(user=user, job="Yönetim", is_active=True, company=create_company, phone=phone)
            user_login(request, user)
            return redirect('index')  # Başarıyla kayıt olduktan sonra anasayfaya yönlendir
        else:
            return render(request, 'login/register.html', {'error': 'Parolalar eşleşmiyor'})
    else:
        return render(request, 'login/register.html')

@login_required
def logout(request):
    user_logout(request)
    return redirect('login')

@login_required
def pricing(request):


    return render(request, 'login/pricing.html')
from django.contrib import messages  # Kullanıcıya bilgi mesajı göstermek için


from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from Core.models import *
from LoginApp.models import *
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404
from .forms import *
from Core.models import CITY_CHOICES
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
import openpyxl


# 404 handler function
def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404


@login_required(login_url='auth_login')
def operation_create(request):
    # Kullanıcının Employee kaydını al
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return render(request, 'error.html', {'message': 'Employee record not found'})

    if request.method == "POST":
        employee_follow = Personel.objects.get(id=request.POST.get('employee_follow'))
        buyer_company = Buyercompany.objects.get(id=request.POST.get('buyer_company'))
        operation_ticket = request.POST.get('operation_ticket')
        passenger_number = request.POST.get('passenger_number')
        start_at = datetime.strptime(request.POST.get('start_at'), '%Y-%m-%d')
        finish_at = datetime.strptime(request.POST.get('finish_at'), '%Y-%m-%d')

        sales_prices = request.POST.getlist('sales_price')
        sales_currency = request.POST.getlist('sales_currency')
        customer_name = request.POST.getlist('customer_name')
        customer_passport = request.POST.getlist('customer_passport')
        date_of_birth = request.POST.getlist('date_of_birth')
        customer_phone = request.POST.getlist('customer_phone')

        if operation_ticket:
            operation = Operation.objects.create(
                company=employee.company,
                selling_staff=employee,
                follow_staff=employee_follow,
                buyer_company=buyer_company,
                ticket=operation_ticket,
                start=start_at,
                finish=finish_at,
                number_passengers=passenger_number
            )
        else:
            operation = Operation.objects.create(
                company=employee.company,
                selling_staff=employee,
                follow_staff=employee_follow,
                buyer_company=buyer_company,
                start=start_at,
                finish=finish_at,
                number_passengers=passenger_number
            )

        for price, currency in zip(sales_prices, sales_currency):
            Salesprice.objects.create(
                company=employee.company,
                operation=operation,
                price=price,
                currency=currency
            )

        for name, pasaport, birth, phone in zip(customer_name, customer_passport, date_of_birth, customer_phone):
            Customer.objects.create(
                company=employee.company,
                operation=operation,
                name=name,
                pasaport=pasaport,
                date_of_birth=datetime.strptime(birth, '%Y-%m-%d'),
                phone=phone
            )

        current_date = start_at
        counter = 1
        while current_date <= finish_at:
            Operationday.objects.create(
                day_number = counter,
                company=employee.company,
                operation=operation,
                date=current_date
            )
            counter+=1
            current_date += timedelta(days=1)
        context = {
            'day' : start_at,
            'day_number' : 1,
            'employees' : Personel.objects.filter(company = employee.company),
            'title': 'Operation Create',
            'company_name': employee.company.name.upper(),
            'operation': operation,
            'form' : OperationitemCreateForm()
        }
        return render(request, 'includes/operations/operation-day-form.html', context)

    else:
        context = {
            'employees' : Personel.objects.filter(company = employee.company, is_delete=False).order_by('user__first_name'),
            'buyer_companies' : Buyercompany.objects.filter(company = employee.company, is_delete=False).order_by('name'),
            'title': 'Operation Create',
            'company_name': employee.company.name.upper(),
        }
        return render(request, 'operations/operation-create/operation-create.html', context)

@login_required(login_url='auth_login')
def operation_day_create(request):
    employee = Personel.objects.get(user=request.user)
    context={
        'title' : 'Operation Day Create',
        'company_name' : employee.company.name.upper(),
        'form' : OperationitemCreateForm()
    }
    return render(request, 'includes/operations/operation-day-form.html', context)

@login_required(login_url='auth_login')
def operation_item_create(request, operation_id, day_number=None):
    employee = Personel.objects.get(user=request.user)
    operation = get_object_or_404(Operation, id=operation_id)

    if request.method == 'POST':
        form = OperationitemCreateForm(request.POST)
        if form.is_valid():
            # Mevcut bir day_number var mı kontrol et
            if day_number:
                operation_day = operation.days.filter(day_number=day_number).first()
                if not operation_day:
                    context = {
                        'operation_id': operation_id,
                        'title': 'Operation Created Completed',
                        'company_name': employee.company.name.upper(),
                        'day_number': day_number + 1,
                        'operation': operation,
                        'form': OperationitemCreateForm()
                    }
                    return render(request, 'includes/operations/operation_create_completed.html', context)

                # Alınan verileri aynı güne kaydet
                operation_item = form.save(commit=False)
                operation_item.company = employee.company
                operation_item.day = operation_day
                operation_item.save()

                # Many-to-many alanlarını kaydet
                form.save_m2m()

                # Bir sonraki gün numarasını kontrol et ve formu yeniden yükle
                next_day_number = day_number + 1
                if operation.days.filter(day_number=next_day_number).exists():
                    day = get_object_or_404(Operationday, operation=operation, day_number=next_day_number)
                    context = {
                        'operation_id': operation_id,
                        'day_number': next_day_number,
                        'operation': operation,
                        'company_name': employee.company.name.upper(),
                        'day': day,
                        'form': OperationitemCreateForm()
                    }
                    return render(request, 'includes/operations/operation-day-form.html', context)
                else:
                    context = {
                        'operation_id': operation_id,
                        'title': 'Operation Created Completed',
                        'company_name': employee.company.name.upper(),
                        'operation': operation,
                        'form': OperationitemCreateForm()
                    }
                    return render(request, 'includes/operations/operation-create-completed.html', context)
            else:
                operation_day = operation.days.first()
                operation_item = form.save(commit=False)
                operation_item.company = employee.company
                operation_item.day = operation_day
                operation_item.save()

                # Many-to-many alanlarını kaydet
                form.save_m2m()

                context = {
                    'operation_id': operation_id,
                    'day_number': 2,
                    'operation': operation,
                    'company_name': employee.company.name.upper(),
                    'day': operation_day,
                    'form': OperationitemCreateForm()
                }
                return render(request, 'includes/operations/operation-day-form.html', context)
        else:
            print(form.errors)
            context = {
                'operation_id': operation_id,
                'title': 'Operation Item Create',
                'company_name': employee.company.name.upper(),
                'operation': operation,
                'day_number': day_number,
                'form': form
            }
            return render(request, 'includes/operations/operation-item-form.html', context)
    else:
        form = OperationitemCreateForm()
        context = {
            'title': 'Operation Item Create',
            'company_name': employee.company.name.upper(),
            'operation': operation,
            'operation_id': operation_id,
            'day_number': day_number,
            'form': OperationitemCreateForm()
        }
        return render(request, 'includes/operations/operation-item-form.html', context)


@login_required(login_url='auth_login')
def operation_create_completed(request, operation_id):
    employee = Personel.objects.get(user=request.user)
    operation = get_object_or_404(Operation, id=operation_id)
    context = {
        'title': 'Operation Create Complated',
        'company_name': employee.company.name.upper(),
        'operation': operation,
    }
    return render(request, 'includes/operations/operation_create_completed.html', context)
@login_required(login_url='auth_login')
def get_customers(request):
    return render(request, 'includes/operations/customer_div.html')

@login_required(login_url='auth_login')
def get_prices(request):
    return render(request, 'includes/operations/sales_div.html')

@login_required(login_url='auth_login')
def customers(request):
    employee = Personel.objects.get(user=request.user)
    customers = Customer.objects.filter(is_delete=False, company=employee.company).order_by('operation__ticket')
    context={
        'title': 'Customers',
        'company_name': employee.company.name.upper(),
        'customers' : customers
    }
    return render(request, 'customers/customers.html', context)


@login_required
def generic_view(request, model):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    ModelClass = globals()[model]
    queryset = ModelClass.objects.filter(company=sirket, is_delete=False)
    form = globals()[f"{model}Form"]()
    fields = ModelClass._meta.fields
    objects_data = []

    # Fields listesine cities eklemek için model kontrolü
    field_names = [field.name for field in fields]
    if model == "Supplier" or model == "Activitysupplier":
        field_names.append('cities')

    for obj in queryset:
        obj_data = {}
        for field in fields:
            obj_data[field.name] = getattr(obj, field.name)

        # Eğer model Vehiclesupplier veya Activitysupplier ise şehir bilgilerini ekle
        if model == "Supplier":
            cities = VehiclesupplierCities.objects.filter(supplier=obj).values_list('city', flat=True)
            obj_data['cities'] = list(cities)
        elif model == "Activitysupplier":
            cities = ActivitysupplierCities.objects.filter(supplier=obj).values_list('city', flat=True)
            obj_data['cities'] = list(cities)

        objects_data.append(obj_data)

    cities = [{'id': city[0], 'name': city[1]} for city in CITY_CHOICES]
    context = {
        'title': model.capitalize(),
        'createtitle': f'CREATE {model.upper()}',
        'listTitle': f'{model.upper()} LIST',
        'createUrl': f'create_{model.lower()}',
        'deleteUrl': f'delete_{model}',
        'form': form,
        'objects_data': objects_data,  # Model nesnelerinin alan değerlerini içeren liste
        'models': queryset,  # Model nesneleri
        'fields': field_names,  # Alan başlıkları
        'model_name': model,
        'number_of_columns': len(field_names) + 1,
        'cities': cities,
        'company_name': requestPersonel.company.name.upper(),
    }

    return render(request, f'files/generic.html', context)



from django.apps import apps
from django.http import HttpResponseNotFound

@login_required
def generic_create_view(request, model):
    request_personnel = Personel.objects.get(user=request.user)
    company = request_personnel.company
    model_class = globals().get(model.capitalize())
    cities = [{'id': city[0], 'name': city[1]} for city in CITY_CHOICES]
    if model_class is None:
        return HttpResponseNotFound(f"{model.capitalize()} model not found")

    form_class = globals().get(f"{model.capitalize()}Form")
    if form_class is None:
        return HttpResponseNotFound(f"{model.capitalize()}Form not found")

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            try:
                new_object = form.save(commit=False)
                new_object.company = company
                new_object.save()
            except Exception as e:
                return HttpResponseServerError(f"Error saving the object: {e}")

            obj_data = {'id': new_object.id}
            for field in model_class._meta.fields:
                obj_data[field.name] = getattr(new_object, field.name)

            field_names = [field.name for field in model_class._meta.fields]

            action_description = f"{model.capitalize()} oluşturdu. ID: {new_object.id}"
            try:
                log = UserActivityLog(
                    company=company,
                    staff=request_personnel,
                    action=action_description,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    browser_info=request.META.get('HTTP_USER_AGENT'),
                )
                log.save()
            except Exception as e:
                return HttpResponseServerError(f"Error logging activity: {e}")


            context = {
                'fields': field_names,  # Alan başlıkları, cities dahil
                'obj_data': obj_data,
                'model_name': model,
                'company_name': request_personnel.company.name.upper(),
            }
            return render(request, 'includes/generics/generic-lists.html', context)
        else:
            errors = form.errors.get_json_data()
            action_description = f"{model.capitalize()} Kayıt Oluşturulamadı. Hata: {errors}"
            log = UserActivityLog(
                company=company,
                staff=request_personnel,
                action=action_description,
                ip_address=request.META.get('REMOTE_ADDR'),
                browser_info=request.META.get('HTTP_USER_AGENT'),
            )
            log.save()

    else:
        form = form_class()
    context = {
        'form': form,
        'model_name': model,
        'cities': cities,
        'company_name': request_personnel.company.name.upper(),
    }
    return render(request, 'includes/generics/generic-forms.html', context)




def add_cities(request, model):
    print("add_cities fonksiyonu çağrıldı.")
    requestPersonel = Personel.objects.get(user=request.user)
    print(f"Kullanıcı: {request.user.username}, Şirket: {requestPersonel.company.name}")

    sirket = requestPersonel.company

    ModelClass = globals().get(model)
    if not ModelClass:
        print(f"ModelClass bulunamadı: {model}")
        return HttpResponseNotFound("Model not found")
    print(f"ModelClass: {ModelClass}")

    queryset = ModelClass.objects.filter(company=sirket, is_delete=False)
    print(f"Queryset oluşturuldu, nesne sayısı: {queryset.count()}")

    form_class = globals().get(f"{model}Form")
    if not form_class:
        print(f"Form class bulunamadı: {model}Form")
        return HttpResponseNotFound("Form not found")
    form = form_class()
    print(f"Form oluşturuldu: {form_class}")

    fields = ModelClass._meta.fields
    objects_data = []
    for obj in queryset:
        obj_data = {}
        for field in fields:
            obj_data[field.name] = getattr(obj, field.name)
        objects_data.append(obj_data)
    print(f"Objects data: {objects_data}")
    cities = [{'id': city[0], 'name': city[1]} for city in CITY_CHOICES]
    context = {
        'title': model.capitalize(),
        'createtitle': f'CREATE {model.upper()}',
        'listTitle': f'{model.upper()} LIST',
        'createUrl': f'create_{model.lower()}',
        'deleteUrl': f'delete_{model}',
        'form': form,
        'objects_data': objects_data,  # Model nesnelerinin alan değerlerini içeren liste
        'models': queryset,  # Model nesneleri
        'fields': [field.name for field in fields],
        'model_name': model,  # Alan başlıkları
        'number_of_columns': len(fields) + 1,
        'cities' : cities,
        'company_name': requestPersonel.company.name.upper(),
    }

    print("Context oluşturuldu, template render ediliyor.")
    return render(request, 'includes/generics/cities.html', context)

@login_required
def generic_edit_view(request, model, obj_id):
    # Model sınıfını dinamik olarak yükle
    ModelClass = globals().get(model.capitalize())
    if ModelClass is None:
        return HttpResponseNotFound(f"{model.capitalize()} model not found.")

    # Model objesini getir veya 404 döndür
    obj = get_object_or_404(ModelClass, id=obj_id)
    request_personnel = Personel.objects.get(user=request.user)
    company = request_personnel.company
    cities_model = [{'id': city[0], 'name': city[1]} for city in CITY_CHOICES]

    # Form sınıfını dinamik olarak yükle
    FormClass = globals().get(f"{model.capitalize()}Form")
    if FormClass is None:
        return HttpResponseNotFound(f"{model.capitalize()}Form not found.")

    # Başlangıçta obj_data ve field_names değişkenlerini tanımla
    obj_data = {'id': obj_id}
    field_names = [field.name for field in ModelClass._meta.fields]

    cityform = None
    if request.method == "POST":
        original_data = {field.name: getattr(obj, field.name) for field in ModelClass._meta.fields}
        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            updated_obj = form.save()
            updated_data = {field.name: getattr(updated_obj, field.name) for field in ModelClass._meta.fields}
            changes = [
                f"{key}: {original_data[key]} den {updated_data[key]} ye değişti"
                for key in original_data if original_data[key] != updated_data[key]
            ]

            if changes:
                action_description = f"Güncellendi. {model.capitalize()} {obj_id}: " + ", ".join(changes)
                log = UserActivityLog(
                    company=company,
                    staff=request_personnel,
                    action=action_description,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    browser_info=request.META.get('HTTP_USER_AGENT'),
                )
                log.save()

            # Cities için kontrol et ve kaydet/güncelle
            if model == "Supplier":
                city_model = VehiclesupplierCities
            elif model == "Activitysupplier":
                city_model = ActivitysupplierCities
            else:
                city_model = None

            if city_model:
                city_ids = request.POST.getlist('city_ids')
                city_names = request.POST.getlist('city')

                # İlk olarak mevcut city_ids için güncelleme işlemi yapıyoruz.
                if city_ids and city_names:
                    for index, city_id in enumerate(city_ids):
                        try:
                            city_name = city_names[index]
                            city_instance = city_model.objects.get(supplier=obj, id=city_id)
                            if city_instance:
                                city_instance.city = city_name
                                city_instance.save()
                        except city_model.DoesNotExist:
                            print(f"City instance with id {city_id} does not exist.")
                        except Exception as e:
                            print(f"Hata oluştu: {e}")

                # Eğer city_names listesinde, city_ids'ten fazla eleman varsa, bunlar yeni kayıt olarak eklenir.
                if len(city_names) > len(city_ids):
                    for index in range(len(city_ids), len(city_names)):
                        city_name = city_names[index]
                        if city_name:
                            try:
                                city_instance = city_model.objects.create(supplier=obj, city=city_name)
                                print(f"Yeni kayıt oluşturuldu: {city_instance}")
                            except Exception as e:
                                print(f"Yeni kayıt oluşturulurken hata oluştu: {e}")

                # Objeye bağlı şehirleri al
                cities = city_model.objects.filter(supplier=obj)
                city_names = [city.city for city in cities]
                obj_data['cities'] = city_names
                field_names.append('cities')

            # Güncellenmiş obje verileri ile context oluştur
            obj_data.update({field.name: getattr(updated_obj, field.name) for field in ModelClass._meta.fields})
            context = {
                'form': form,
                'obj_data': obj_data,
                'model_name': model,
                'fields': field_names,
                'company_name': request_personnel.company.name.upper(),
                'cityform': cityform,
            }
            return render(request, 'includes/generics/generic-lists.html', context)
        else:
            print(form.errors)
    else:
        if model.lower() == 'personel':
            initial_data = {
                'username': obj.user.username,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'email': obj.user.email,
            }
            form = FormClass(instance=obj, initial=initial_data)
        else:
            form = FormClass(instance=obj)

        city_name = None
        if model == "Supplier":
            city_model = VehiclesupplierCities
            cityform = VehiclesupplierCitiesForm()
        elif model == "Activitysupplier":
            city_model = ActivitysupplierCities
            cityform = ActivitysupplierCitiesForm()
        else:
            city_model = None

        if city_model:
            city_instance = city_model.objects.filter(supplier=obj)


        context = {
            'form': form,
            'obj_data': obj,
            'model_name': model,
            'fields': field_names,
            'number_of_columns': len(field_names) + 5,
            'company_name': request_personnel.company.name.upper(),
            'cityform': cityform,
            'city_instance' : city_instance,
            'cities_model' : cities_model,
        }

    return render(request, 'includes/generics/generic-edit-forms.html', context)



@login_required
def generic_delete_view(request, model, obj_id):
    ModelClass = globals().get(model.capitalize())
    if ModelClass is None:
        return HttpResponseNotFound(f"{model.capitalize()} model not found.")

    # Model objesini getir veya 404 döndür
    obj = get_object_or_404(ModelClass, id=obj_id)
    request_personnel = Personel.objects.get(user=request.user)
    company = request_personnel.company

    if request.method == "DELETE":
        obj_data = {field.name: getattr(obj, field.name) for field in ModelClass._meta.fields}
        transfer = get_object_or_404(ModelClass, id=obj_id)
        try:
            transfer.is_delete = True
            transfer.save()
            action_description = f"Silindi {model.capitalize()} {obj_id}: " + ", ".join([f"{key}: {value}" for key, value in obj_data.items()])
            log = UserActivityLog(
                company=company,
                staff=request_personnel,
                action=action_description,
                ip_address=request.META.get('REMOTE_ADDR'),  # Kullanıcının IP adresini alır
                browser_info=request.META.get('HTTP_USER_AGENT'),  # Kullanıcının tarayıcı bilgilerini alır
            )
            log.save()

            return HttpResponse('')
        except Personel.DoesNotExist:
            pass  # veya uygun bir hata mesajı göster
          # Boş bir yanıt döndür


@login_required
def generic_cancel_view(request, model, obj_id):
    request_personnel = Personel.objects.get(user=request.user)

    ModelClass = globals().get(model.capitalize())
    if ModelClass is None:
        return HttpResponseNotFound(f"{model.capitalize()} model not found.")

    # Model objesini getir veya 404 döndür
    obj = get_object_or_404(ModelClass, id=obj_id)

    # Objeden alınan verileri saklamak için dictionary oluştur
    obj_data = {'id': obj_id}
    for field in ModelClass._meta.fields:
        obj_data[field.name] = getattr(obj, field.name)

    # Şehir isimlerini topla ve alan isimlerini ayarla
    city_names = []
    if model == "Supplier":
        cities = VehiclesupplierCities.objects.filter(supplier=obj)
    elif model == "Activitysupplier":
        cities = ActivitysupplierCities.objects.filter(supplier=obj)
    else:
        cities = []

    if  model == "Supplier" or model == "Activitysupplier":
        city_names = [city.city for city in cities]
        obj_data['cities'] = city_names
        field_names = [field.name for field in ModelClass._meta.fields]
        field_names.append('cities')
    else:
        field_names = [field.name for field in ModelClass._meta.fields]

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'includes/generics/generic-lists.html', {
        'obj_data': obj_data,
        'fields': field_names,
        'model_name': model,
        'company_name': request_personnel.company.name.upper()
    })

def format_date(date):
    return date.strftime("%d.%m.%Y")

@login_required
def jobs(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        startDate = request.POST.get('startDate')
        dueDate = request.POST.get('dueDate')
        if not startDate:
            return redirect('jobs')
        if dueDate:
            formated_startDate = timezone.datetime.strptime(startDate, '%Y-%m-%d').date()
            formated_dueDate = timezone.datetime.strptime(dueDate, '%Y-%m-%d').date()
            jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date__range=(startDate, dueDate)).order_by('pick_time')
            today = f"{format_date(formated_startDate)} - {format_date(formated_dueDate)}"
            context = {
                'title': 'Jobs',
                'today' : today,
                'jobs': jobs,
                'date_input' : True,
                'company_name': employee.company.name.upper(),
            }
        else:
            formated_startDate = timezone.datetime.strptime(startDate, '%Y-%m-%d').date()
            jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=startDate).order_by('pick_time')
            context = {
                'title': 'Jobs',
                'today' : format_date(formated_startDate),
                'jobs': jobs,
                'date_input' : True,
                'company_name': employee.company.name.upper(),
            }
        return render(request, 'jobs/job-lists.html', context)
    else:
        today = timezone.now().date()
        jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=today).order_by('pick_time')
        tomorrow = today + timezone.timedelta(days=1)
        day_after_tomorrow = today + timezone.timedelta(days=2)
        tomorrow_jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=tomorrow).order_by('pick_time')
        day_after_tomorrow_jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=day_after_tomorrow).order_by('pick_time')
        formated_today = format_date(today)
        context = {
            'title': 'Jobs',
            'today' : formated_today,
            'tomorrow' : tomorrow,
            'day_after_tomorrow' : day_after_tomorrow,
            'jobs': jobs,
            'tomorrow_jobs': tomorrow_jobs,
            'date_input' : False,
            'day_after_tomorrow_jobs': day_after_tomorrow_jobs,
            'company_name': employee.company.name.upper(),
        }
        return render(request, 'jobs/job-lists.html', context)

@login_required
def my_jobs(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        startDate = request.POST.get('startDate')
        dueDate = request.POST.get('dueDate')
        if dueDate:
            formated_startDate = timezone.datetime.strptime(startDate, '%Y-%m-%d').date()
            formated_dueDate = timezone.datetime.strptime(dueDate, '%Y-%m-%d').date()
            jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date__range=(startDate, dueDate), day__operation__follow_staff=employee).order_by('pick_time')
            today = f"{format_date(formated_startDate)} - {format_date(formated_dueDate)}"
            context = {
                'title': 'Jobs',
                'today' : today,
                'jobs': jobs,
                'date_input' : True,
                'company_name': employee.company.name.upper(),
            }
        else:
            formated_startDate = timezone.datetime.strptime(startDate, '%Y-%m-%d').date()
            jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=startDate, day__operation__follow_staff=employee).order_by('pick_time')
            context = {
                'title': 'Jobs',
                'today' : format_date(formated_startDate),
                'jobs': jobs,
                'date_input' : True,
                'company_name': employee.company.name.upper(),
            }
        return render(request, 'jobs/job-lists.html', context)
    else:
        today = timezone.now().date()
        jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=today, day__operation__follow_staff=employee).order_by('pick_time')
        tomorrow = today + timezone.timedelta(days=1)
        day_after_tomorrow = today + timezone.timedelta(days=2)
        tomorrow_jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=tomorrow, day__operation__follow_staff=employee).order_by('pick_time')
        day_after_tomorrow_jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=day_after_tomorrow, day__operation__follow_staff=employee).order_by('pick_time')
        formated_today = format_date(today)
        context = {
            'title': 'My Jobs',
            'date_input' : False,
            'today' : formated_today,
            'tomorrow' : tomorrow,
            'day_after_tomorrow' : day_after_tomorrow,
            'jobs': jobs,
            'tomorrow_jobs': tomorrow_jobs,
            'day_after_tomorrow_jobs': day_after_tomorrow_jobs,
            'company_name': employee.company.name.upper(),
        }
        return render(request, 'jobs/job-lists.html', context)

def update_operationitem(request, pk):
    item = get_object_or_404(Operationitem, pk=pk)
    if request.method == 'POST':
        form = OperationitemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return render(request, 'includes/jobs/item-details-row.html', {'item': item})
        else:
            print(form.errors)
            return render(request, 'includes/jobs/jobs-update.html', {'form': form, 'item': item})
    else:
        form = OperationitemForm(instance=item)
        return render(request, 'includes/jobs/jobs-update.html', {'form': form, 'item': item})




def operation_lists(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    month = datetime.now().month
    buyer_companies = Buyercompany.objects.filter(company=employee.company, is_delete=False).order_by('-name')
    context = {
        'title': 'Operation Lists',
        'buyer_companies' : buyer_companies,
        'month' : month,
        'company_name': employee.company.name.upper(),
    }
    return render(request, 'operations/operation-lists/operation-lists.html', context)


def operation_list_details(request, company_id, month=None):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")

    company = get_object_or_404(Buyercompany, id=company_id)

    # Eğer 'month' parametresi 0 veya None ise bugünün ayını kullan
    if month is None or month == 0:
        month = datetime.now().month

    operations = Operation.objects.filter(buyer_company=company, is_delete=False, finish__month=month)
    context = {
        'title': 'Operation Lists',
        'company_id' : company_id,
        'company' : company,
        'operations' : operations,
        'month' : month,
        'company_name': employee.company.name.upper(),
    }
    return render(request, 'operations/operation-lists/operation-list-detail.html', context)



def operation_ticket_lists(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    today = timezone.now().date()
    operations = Operation.objects.filter(company=employee.company, is_delete=False).order_by("-start")
    for operation in operations:
        if operation.finish >= today and operation.start > today:
            operation.cont = "Future"
        elif operation.start <= today and operation.finish >= today:
            operation.cont = "Continious"
        elif operation.finish < today:
            operation.cont = "Completed"
    context = {
        'title': 'Operation Ticket Lists',
        'operations' : operations,
        'company_name': employee.company.name.upper(),
    }
    return render(request, 'operations/operation-lists/operation-ticket-lists.html', context)


def operation_ticket_list_details(request, operation_id):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")

    operation = get_object_or_404(Operation, id=operation_id)
    days = Operationday.objects.filter(operation=operation, is_delete=False)
    for day in days:
        day.items_filtered = day.items.filter(is_delete=False)

    context = {
        'title': 'Operation Ticket Lists',
        'operation_id' : operation_id,
        'operation' : operation,
        'days' : days,
        'company_name': employee.company.name.upper(),
    }
    return render(request, 'operations/operation-lists/operation-ticket-list-detail.html', context)

def export_operation_to_excel(request, operation_id):
    # Operasyon verilerini al
    operation = Operation.objects.get(id=operation_id)
    days = Operationday.objects.filter(operation=operation, is_delete=False)

    # Yeni bir Excel çalışma kitabı oluştur
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Operation Data'

    # Başlıkları ekle
    headers = [
        'Ticket', 'Start Date', 'Finish Date', 'Sold Employee', 'Follow Employee', 'Created Date', 'Prices', 'Customers',
        'Day', 'Operation Type', 'Description', 'Pick-up Time', 'Pick-up Point',
        'Tour', 'Transfer', 'Vehicle Type', 'Vehicle Supplier', 'Vehicle Cost Price', 'Vehicle Sell Price',
        'Hotel', 'Room Type', 'Hotel Cost Price', 'Hotel Sell Price', 'Hotel Payment',
        'Museums', 'Museums Cost Price', 'Museums Sell Price', 'Museums Payment',
        'Activity', 'Activity Supplier', 'Activity Cost Price', 'Activity Sell Price', 'Activity Payment',
        'Guide', 'Guide Cost Price', 'Guide Sell Price', 'There is Guide',
        'Driver Name', 'Driver Phone', 'Vehicle Plate',
        'Other Cost Price', 'Other Sell Price'
    ]
    sheet.append(headers)

    # Verileri ekle
    for day in days:
        for item in day.items.filter(is_delete=False):
            row = [
                operation.ticket or '---',
                operation.start.strftime('%d.%m.%Y') if operation.start else '---',
                operation.finish.strftime('%d.%m.%Y') if operation.finish else '---',
                operation.selling_staff.user.username if operation.selling_staff else '---',
                operation.follow_staff.user.username if operation.follow_staff else '---',
                operation.create_date.strftime('%d.%m.%Y %H:%M') if operation.create_date else '---',
                ', '.join([f"{price.price} {price.currency}" for price in operation.prices.all()]) if operation.prices.exists() else '---',
                ', '.join([f"{customer.name} - {customer.phone}" for customer in operation.customers.all()]) if operation.customers.exists() else '---',
                day.date.strftime('%d.%m.%Y') if day.date else '---',
                item.operation_type or '---',
                item.description or '---',
                item.pick_time or '---',
                item.pick_location or '---',
                item.tour.route if item.tour and item.tour.route else '---',
                item.transfer.route if item.transfer and item.transfer.route else '---',
                item.vehicle.vehicle if item.vehicle else '---',
                item.supplier or '---',
                item.vehicle_price or '---',
                item.vehicle_sell_price or '---',
                item.hotel.name if item.hotel else '---',
                item.room_type or '---',
                item.hotel_price or '---',
                item.hotel_sell_price or '---',
                item.hotel_payment or '---',
                ', '.join([museum.name for museum in item.new_museum.all()]) if item.new_museum.exists() else '---',
                item.museum_price or '---',
                item.museum_sell_price or '---',
                item.museum_payment or '---',
                item.activity.name if item.activity else '---',
                item.activity_supplier or '---',
                item.activity_price or '---',
                item.activity_sell_price or '---',
                item.activity_payment or '---',
                item.guide.name if item.guide else '---',
                item.guide_price or '---',
                item.guide_sell_price or '---',
                item.guide_var or '---',
                item.driver or '---',
                item.driver_phone or '---',
                item.plaka or '---',
                item.other_price or '---',
                item.other_sell_price or '---'
            ]
            sheet.append(row)

    # Response ayarları
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={operation.ticket}_operation_data.xlsx'

    # Excel dosyasını response'a yaz
    workbook.save(response)
    return response

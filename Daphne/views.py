from django.shortcuts import render, redirect
from django.utils import timezone
from Core.models import *
from Core.forms import *

def format_date(date):
    return date.strftime("%d.%m.%Y")

def jobs(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        startDate = request.POST.get('startDate')
        dueDate = request.POST.get('dueDate')
        if not startDate:
            return redirect('daphne_jobs')
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
            }
        else:
            formated_startDate = timezone.datetime.strptime(startDate, '%Y-%m-%d').date()
            jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=startDate).order_by('pick_time')
            context = {
                'title': 'Jobs',
                'today' : format_date(formated_startDate),
                'jobs': jobs,
                'date_input' : True,
            }
        return render(request, 'pages/jobs/job-lists.html', context)
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
        }
        return render(request, 'pages/jobs/job-lists.html', context)
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
            }
        else:
            formated_startDate = timezone.datetime.strptime(startDate, '%Y-%m-%d').date()
            jobs = Operationitem.objects.filter(company=employee.company, is_delete=False, day__date=startDate, day__operation__follow_staff=employee).order_by('pick_time')
            context = {
                'title': 'Jobs',
                'today' : format_date(formated_startDate),
                'jobs': jobs,
                'date_input' : True,
            }
        return render(request, 'pages/jobs/job-lists.html', context)
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
        }
        return render(request, 'pages/jobs/job-lists.html', context)
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse

def tours(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        route_name = request.POST.get('route_name')
        if route_name:
            route_name = route_name.upper()
        else:
            return HttpResponseBadRequest("Route name is required.")

        locations = request.POST.getlist('location')
        if not locations:
            return HttpResponseBadRequest("At least one location is required.")

        tour = Tour.objects.create(company=employee.company, route=route_name)
        for location in locations:
            lct = Konum.objects.filter(route=location).first()
            if lct:
                TourRoute.objects.create(company=employee.company, tour=tour, konum=lct)

        tours = Tour.objects.filter(is_delete=False).order_by('route')
        for tour in tours:
            tour.routes = TourRoute.objects.filter(tour=tour, is_delete=False)
        context = {
            'title': 'Tours',
            'tours': tours,
            'tour': tour,
            'locations': True,
            'submit_url': reverse('daphne_tours')
        }
        return render(request, 'includes/files/tours/tour-table.html', context)
    else:
        tours = Tour.objects.filter(company=employee.company, is_delete=False).order_by('route')
        for tour in tours:
            tour.routes = TourRoute.objects.filter(tour=tour, is_delete=False)
        locations = Konum.objects.filter(company=employee.company, is_delete=False).order_by('route')
        context = {
            'title': 'Tours',
            'tours': tours,
            'locations_select': locations,
            'locations': False,
            'submit_url': reverse('daphne_tours')
        }
        return render(request, 'pages/files/tours.html', context)


def transfers(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        route_name = request.POST.get('route_name')
        if route_name:
            route_name = route_name.upper()
        else:
            return HttpResponseBadRequest("Route name is required.")

        locations = request.POST.getlist('location')
        if not locations:
            return HttpResponseBadRequest("At least one location is required.")

        tour = Transfer.objects.create(company=employee.company, route=route_name)
        for location in locations:
            lct = Konum.objects.filter(route=location).first()
            if lct:
                TransferRoute.objects.create(company=employee.company, transfer=tour, konum=lct)

        tours = Transfer.objects.filter(is_delete=False).order_by('route')
        for tour in tours:
            tour.routes = TransferRoute.objects.filter(transfer=tour, is_delete=False)
        context = {
            'title': 'Transfers',
            'tours': tours,
            'tour': tour,
            'locations': True,
            'submit_url': reverse('daphne_transfers')
        }
        return render(request, 'includes/files/tours/tour-table.html', context)
    else:
        tours = Transfer.objects.filter(company=employee.company, is_delete=False).order_by('route')
        for tour in tours:
            tour.routes = TransferRoute.objects.filter(transfer=tour, is_delete=False)
        locations = Konum.objects.filter(is_delete=False).order_by('route')
        context = {
            'title': 'Transfer',
            'tours': tours,
            'locations_select': locations,
            'locations': False,
            'submit_url': reverse('daphne_transfers')
        }
        return render(request, 'pages/files/tours.html', context)

def locations(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        route_name = request.POST.get('route_name').upper()

        employee = Personel.objects.get(user=request.user)
        tour = Konum.objects.create(company=employee.company, route=route_name)
        tours = Konum.objects.filter(is_delete=False).order_by('route')
        context={
            'title' : 'Locations',
            'tours' : tours,
            'tour' : tour,
            'locations' : True,
            'submit_url' : reverse('daphne_locations')
        }
        return render(request, 'includes/files/tours/tour-table.html', context)

    else:
        tours = Konum.objects.filter(company=employee.company, is_delete=False).order_by('route')
        context={
            'title' : 'Locations',
            'tours' : tours,
            'locations' : True,
            'submit_url' : reverse('daphne_locations')
        }
        return render(request, 'pages/files/tours.html', context)

def tourroute(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    locations = Konum.objects.filter(company=employee.company, is_delete=False).order_by('route')

    return render(request, 'includes/files/tours/tour-route.html',{'locations_select' : locations})


def vehicles(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == "POST":
        vehicle_name = request.POST.get('vehicle_name').upper()
        capacity = request.POST.get('capacity')


        vehicle = Vehicle.objects.create(company=employee.company, vehicle=vehicle_name, capacity=capacity)
        vehicles = Vehicle.objects.filter(is_delete = False)
        context={
            'title' : 'Vehicles',
            'tours' : vehicles,
            'tour' : vehicle,
            'submit_url' : reverse('daphne_vehicles')
        }
        return render(request, 'includes/files/vehicles/vehicle-table.html', context)

    else:
        vehicles = Vehicle.objects.filter(company=employee.company, is_delete = False)
        context={
            'title' : 'Vehicles',
            'tours' : vehicles,
            'submit_url' : reverse('daphne_vehicles')
        }
        return render(request, 'pages/files/vehicle.html', context)


def guides(request):
    try:
        employee = Personel.objects.get(user=request.user)
    except Personel.DoesNotExist:
        return HttpResponseBadRequest("Employee not found.")
    if request.method == 'POST':
        name = request.POST.get('guide_name').upper()
        location = request.POST.get('location')
        doc_no = request.POST.get('doc_no').upper()
        phone = request.POST.get('phone')
        mail = request.POST.get('email')
        price = request.POST.get('price')
        currency = request.POST.get('currency')
        lct = Konum.objects.filter(route=location).first()
        if lct:
            guide = Guide.objects.create(company=employee.company, name=name, phone=phone, location=lct, city=lct.route, doc_no=doc_no, mail=mail, price=price, currency=currency)
        guides = Guide.objects.filter(is_delete = False, company=employee.company)
        locations = Konum.objects.filter(company=employee.company, is_delete=False).order_by('route')
        context={
            'title' : 'Guides',
            'guide' : guide,
            'guides' : guides,
            'locations' : locations,
            'submit_url' : reverse('daphne_guides')
        }
        return render(request, 'includes/files/guides/guide-table.html', context)

    else:
        guides = Guide.objects.filter(is_delete = False, company=employee.company)
        locations = Konum.objects.filter(company=employee.company, is_delete=False).order_by('route')
        context={
            'title' : 'Guides',
            'guides' : guides,
            'locations' : locations,
            'submit_url' : reverse('daphne_guides')
        }
        return render(request, 'pages/files/guide.html', context)


from django.urls import path, include
from .views import *

urlpatterns = [

    path('jobs', jobs, name="daphne_jobs"),
    path('my-jobs', my_jobs, name='daphne_my_jobs'),
    path('tours', tours, name='daphne_tours'),
    path('transfers', transfers, name='daphne_transfers'),
    path('locations', locations, name='daphne_locations'),
    path('add-location', tourroute, name='daphne_tour_route'),
    path('vehicles', vehicles, name='daphne_vehicles'),
    path('guides', guides, name='daphne_guides'),

    path('jobs/', jobs),
    path('my-jobs/', my_jobs),
    path('tours/', tours),
    path('transfers/', transfers),
    path('add-location/', tourroute),
]
from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.note_list, name='note_list'),
    path('task/', views.task_list, name='task_list'),
    path('shortcut/', views.shortcut_list, name='shortcut_list'),
    path('alarm/', views.alarm_list, name='alarm_list'),
]

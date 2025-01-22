from django.urls import path
from . import views

urlpatterns = [
    path('new/operation-lists/', views.operation_lists, name='operation_lists'),
    path('new/operation-lists-details/<int:company_id>/<int:month>/', views.operation_list_details, name='operation_list_details'),
    path('new/operation-ticket-lists/', views.operation_ticket_lists, name='operation_ticket_lists'),
    path('new/operation-ticket-lists-details/<int:operation_id>/', views.operation_ticket_list_details, name='operation_ticket_list_details'),
    path('new/operation-create/', views.operation_create, name='operation_create'),
    path('new/operation-day-create/', views.operation_day_create, name='operation_day_create'),
    path('new/operation-item-create/<int:operation_id>/', views.operation_item_create, name='operation_item_create'),
    path('new/operation-item-create/<int:operation_id>/<int:day_number>/', views.operation_item_create, name='operation_item_create_day'),
    path('new/operation-create-complated/<int:operation_id>', views.operation_create_completed, name='operation_create_completed'),
    path('new/operation-item-update/<int:pk>', views.update_operationitem, name='update_operationitem'),
    path('get-customer/', views.get_customers, name='get_customers'),
    path('get-prices/', views.get_prices, name='get_prices'),

    path('export/operation/<int:operation_id>/', views.export_operation_to_excel, name='export_operation_to_excel'),


    path('customers/', views.customers, name='customers'),
    path('new/jobs/', views.jobs, name='new_jobs'),
    path('new/my-jobs/', views.my_jobs, name='new_my_jobs'),

    path('generic/<str:model>', views.generic_view, name='generic'),
    path('generic/add_cities/<str:model>', views.add_cities, name='add_cities'),
    path('generic/create/<str:model>', views.generic_create_view, name='new_generic_create_view'),
    path('generic/update/<str:model>/<int:obj_id>', views.generic_edit_view, name='new_generic_edit_view'),
    path('generic/cancel/<str:model>/<int:obj_id>', views.generic_cancel_view, name='new_generic_cancel_view'),
    path('generic/delete/<str:model>/<int:obj_id>', views.generic_delete_view, name='new_generic_delete_view'),

]

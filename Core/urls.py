from django.urls import path
from .views import *
urlpatterns = [
    path('', indexim, name="index"),
    path('jobs/', index, name='jobs'),
    path('my-jobs/', indexim, name='myjobs'),  
    path('logs', logs, name="logs"),
    path('log_staff/<int:personel_id>', log_staff, name="log_staff"),
    path('dark_mode', dark_mode, name="dark_mode"),
    path('main/<str:model>/', generic_view, name='generic_view'),
    path('create/<str:model>/', generic_create_view, name='generic_create_view'),
    path('mobile_create/<str:model>/', generic_mobile_create_view, name='generic_mobile_create_view'),
    path('edit/<str:model>/<int:obj_id>', generic_edit_view, name='generic_edit_view'),
    path('mobile_edit/<str:model>/<int:obj_id>', generic_mobile_edit_view, name='generic_mobile_edit_view'),
    path('delete/<str:model>/<int:obj_id>', generic_delete_view, name='generic_delete_view'),
    path('cancel/<str:model>/<int:obj_id>', generic_cancel_view, name='generic_cancel_view'),
    path('mobile_cancel/<str:model>/<int:obj_id>', generic_mobile_cancel_view, name='generic_mobile_cancel_view'),
    path('operation/', operation, name='operation'),
    path('operation/delete/<int:operation_id>', delete_operation, name='delete_operation'),
    path('operation/item/delete/<int:operation_id>', delete_operationitem, name='delete_operationitem'),
    path('operation/update/<int:operation_id>', update_operation, name='update_operation'),
    path('operation/item/update/<int:day_id>/<int:item_id>', update_or_add_operation_item, name='update_operation_item'),
    path('operation/item/update/<int:day_id>/', update_or_add_operation_item, name='add_operation_item'),
    path('create_operation/', create_operation, name='create_operation'),
    path('create_operation_item_add/', create_operation_item_add, name='create_operation_item_add'),
    path('create_operation_item/<int:day_id>/', create_operation_item, name='create_operation_item'),
    path('operation_list/', operation_list, name='operation_list'),
    path('operation_details/<int:operation_id>/', operation_details, name='operation_details'),
    path('check_ticket/', check_ticket, name='check_ticket'),
    path('template_create/<int:operation_id>', template_create, name='template_create'),
    path('template_list/', template_list, name='template_list'),
    path('notification/create_notification/', create_notification, name='notification_create'),
    path('api/notifications/', notifications_api, name='notifications_api'),
    path('api/mark-notification-read/', mark_notification_as_read, name='mark-notification-read'),


      
]


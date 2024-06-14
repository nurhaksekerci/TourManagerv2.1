from django.urls import path, include
from .views import *


urlpatterns = [

    path('', indexim, name="index"),
    path('jobs/', index, name='jobs'),
    path('my-jobs/', indexim, name='myjobs'),

    path('logs', logs, name="logs"),
    path('log_staff/<int:personel_id>', log_staff, name="log_staff"),
    path('logs/login/', login_logs, name='login_logs'),
    path('logs/staff/<int:personel_id>/login/', log_staff_login, name='log_staff_login'),
    path('dark_mode', dark_mode, name="dark_mode"),

    path('main/<str:model>/', generic_view, name='generic_view'),
    path('create/<str:model>/', generic_create_view, name='generic_create_view'),
    path('delete/<str:model>/<int:obj_id>', generic_delete_view, name='generic_delete_view'),
    path('edit/<str:model>/<int:obj_id>', generic_edit_view, name='generic_edit_view'),
    path('cancel/<str:model>/<int:obj_id>', generic_cancel_view, name='generic_cancel_view'),

    path('mobile_create/<str:model>/', generic_mobile_create_view, name='generic_mobile_create_view'),
    path('mobile_edit/<str:model>/<int:obj_id>', generic_mobile_edit_view, name='generic_mobile_edit_view'),
    path('mobile_cancel/<str:model>/<int:obj_id>', generic_mobile_cancel_view, name='generic_mobile_cancel_view'),
    path('operation/', operation, name='operation'),
    path('operation/delete/<int:operation_id>', delete_operation, name='delete_operation'),
    path('operation/item/delete/<int:operationitem_id>', delete_operationitem, name='delete_operationitem'),
    path('operation/update/<int:operation_id>', update_operation, name='update_operation'),
    path('operation/item/update/<int:day_id>/<int:item_id>', update_or_add_operation_item, name='update_operation_item'),
    path('operation/item/update/<int:day_id>/', add_operation_item, name='add_operation_item'),
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
    path('download-template/<str:model>/', generic_excel_download, name='generic_excel_download'),
    path('download-excel-files/<str:model>/', generic_excel_full_download, name='generic_excel_full_download'),
    path('upload-template/<str:model>/', generic_excel_upload, name='generic_excel_upload'),

    path('get_exchange_rates/', get_exchange_rates, name='get_exchange_rates'),


    path('isler/filtre/', filtre, name='filtre'),
    path('check-cost-duplicate/', check_cost_duplicate, name='check_cost_duplicate'),
    path('check-hotel-duplicate/', check_hotel_duplicate, name='check_hotel_duplicate'),
    path('check-activity-duplicate/', check_activity_duplicate, name='check_activity_duplicate'),
    path('check-transfer-duplicate/', check_transfer_duplicate, name='check_transfer_duplicate'),
    path('check-tour-duplicate/', check_tour_duplicate, name='check_tour_duplicate'),
    path('cari/', cari, name='cari'),
    path('cari/<int:tedarikci_id>/', cari_category, name='cari_category'),
    path('cari/<int:tedarikci_id>/<str:month>/<str:field>/', cari_category, name='cari_category_field'),
    path('activity/cari/<int:tedarikci_id>/<str:month>/<str:field>/', activity_cari_category, name='activity_cari_category_field'),
    path('activity/cari/<int:tedarikci_id>/<str:month>/<str:field>/', activity_cari_category, name='activity_cari_category'),
    path('activity/cari/<int:tedarikci_id>/', activity_cari_category, name='activity_cari_category'),
    path('activity/cari/', activity_cari, name='activity_cari'),

    path('support_ticket/new/', support_ticket_create, name='support_ticket_create'),
    path('support_ticket/<int:sup_id>/', support_cevap, name='support_cevap'),
    path('get-suppliers/<int:item_id>/', get_suppliers, name='get_suppliers'),

    path('ortak_cost/', ortak_cost, name='ortak_cost'),
    path('smsgonder/', smsgonder, name='smsgonder'),


    path('fetch_personnel_list/', fetch_personnel_list, name='fetch_personnel_list'),
    path('fetch_chat_messages/<int:personnel_id>/', fetch_chat_messages, name='fetch_chat_messages'),
    path('send_message/', send_message, name='send_message'),

    path('hata_bildir/', hata_bildir, name='hata_bildir'),
    path('gelir/', gelir, name='gelir'),
    path('grafik/', grafik, name='grafik'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/<int:month_sec>', dashboard, name='dashboardmonth'),
    path('gelir/<int:month>', gelir, name='gelirmonth'),
    path('odeme/', odeme_create, name='odeme_create'),
    path('odeme/guncelle/<int:pk>', odeme_update, name='odeme_update'),
    path('odeme/sil/<int:pk>', odeme_delete, name='odeme_delete'),

]


from django.urls import path
from .views import *

urlpatterns = [

    #Kayıtlar:
    path('companies/', SirketListCreateView.as_view(), name='sirket-list-create'),
    path('companies/<int:pk>/', SirketDetailView.as_view(), name='sirket-detail'),
    path('employees/', PersonelListCreateView.as_view(), name='personel-list-create'),
    path('employees/<int:pk>/', PersonelDetailView.as_view(), name='personel-detail'),
    path('tours/', TourListCreateView.as_view(), name='tour-list-create'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour-detail'),
    path('transfers/', TransferListCreateView.as_view(), name='transfer-list-create'),
    path('transfers/<int:pk>/', TransferDetailView.as_view(), name='transfer-detail'),
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicle-list-create'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('guides/', GuideListCreateView.as_view(), name='guide-list-create'),
    path('guides/<int:pk>/', GuideDetailView.as_view(), name='guide-detail'),
    path('hotels/', HotelListCreateView.as_view(), name='hotel-list-create'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('museums/', MuseumListCreateView.as_view(), name='museum-list-create'),
    path('museums/<int:pk>/', MuseumDetailView.as_view(), name='museum-detail'),
    path('suppliers/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('activitysuppliers/', ActivitysupplierListCreateView.as_view(), name='activitysupplier-list-create'),
    path('activitysuppliers/<int:pk>/', ActivitysupplierDetailView.as_view(), name='activitysupplier-detail'),
    path('buyercompanies/', BuyercompanyListCreateView.as_view(), name='buyercompany-list-create'),
    path('buyercompanies/<int:pk>/', BuyercompanyDetailView.as_view(), name='buyercompany-detail'),
    #Yönetim
    path('costs/', CostListCreateView.as_view(), name='cost-list-create'),
    path('costs/<int:pk>/', CostDetailView.as_view(), name='cost-detail'),
    path('activitycosts/', ActivitycostListCreateView.as_view(), name='activitycost-list-create'),
    path('activitycosts/<int:pk>/', ActivitycostDetailView.as_view(), name='activitycost-detail'),
    #Opersayon İşlemleri
    path('operations/', OperationListCreateView.as_view(), name='operation-list-create'),
    path('operations/<int:pk>/', OperationDetailView.as_view(), name='operation-detail'),
    path('operationdays/', OperationdayListCreateView.as_view(), name='operationday-list-create'),
    path('operationdays/<int:pk>/', OperationdayDetailView.as_view(), name='operationday-detail'),
    path('operationitems/', OperationitemListCreateView.as_view(), name='operationitem-list-create'),
    path('operationitems/<int:pk>/', OperationitemDetailView.as_view(), name='operationitem-detail'),
    #Şablon Opersayon İşlemleri
    path('operation-templates/', OperationTemplateListCreateView.as_view(), name='operationtemplate-list-create'),
    path('operation-templates/<int:pk>/', OperationTemplateDetailView.as_view(), name='operationtemplate-detail'),
    path('operationday-templates/', OperationdayTemplateListCreateView.as_view(), name='operationdaytemplate-list-create'),
    path('operationday-templates/<int:pk>/', OperationdayTemplateDetailView.as_view(), name='operationdaytemplate-detail'),
    path('operationitem-templates/', OperationitemTemplateListCreateView.as_view(), name='operationitemtemplate-list-create'),
    path('operationitem-templates/<int:pk>/', OperationitemTemplateDetailView.as_view(), name='operationitemtemplate-detail'),
    #Döviz kurları:
    path('exchange-rates/', ExchangeRateListCreateView.as_view(), name='exchangerate-list-create'),
    path('exchange-rates/<int:pk>/', ExchangeRateDetailView.as_view(), name='exchangerate-detail'),
    #Bildirimler
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notification-receipts/', NotificationReceiptListCreateView.as_view(), name='notificationreceipt-list-create'),
    path('notification-receipts/<int:pk>/', NotificationReceiptDetailView.as_view(), name='notificationreceipt-detail'),
    #Destek Kayıtları
    path('support-tickets/', SupportTicketListCreateView.as_view(), name='supportticket-list-create'),
    path('support-tickets/<int:pk>/', SupportTicketDetailView.as_view(), name='supportticket-detail'),
    #Sms Gönder:
    path('send-smses/', SmsgonderListCreateView.as_view(), name='smsgonder-list-create'),
    path('send-smses/<int:pk>/', SmsgonderDetailView.as_view(), name='smsgonder-detail'),
    #cari:
    path('cari/', CariListCreateView.as_view(), name='cari-list-create'),
    path('cari/<int:pk>/', CariDetailView.as_view(), name='cari-detail'),
    #Satışlar:
    path('sells/', SellListCreateView.as_view(), name='sell-list-create'),
    path('sells/<int:pk>/', SellDetailView.as_view(), name='sell-detail'),
    path('activitysells/', ActivitysellListCreateView.as_view(), name='activitysell-list-create'),
    path('activitysells/<int:pk>/', ActivitysellDetailView.as_view(), name='activitysell-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('today-operationitems/', TodayOperationItems.as_view(), name='today-operationitems'),
    path('tomorrow-operationitems/', TomorrowOperationItems.as_view(), name='tomorrow-operationitems'),
    path('next-day-operationitems/', NextDayOperationItems.as_view(), name='next-day-operationitems'),


]
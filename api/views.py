from rest_framework import generics, permissions
from django.contrib.auth.models import User
from Core.models import *
from .serializers import *

#Şirket Bilgileri
class SirketListCreateView(generics.ListCreateAPIView):
    queryset = Sirket.objects.filter(is_delete=False)
    serializer_class = SirketSerializer

class SirketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sirket.objects.filter(is_delete=False)
    serializer_class = SirketSerializer

#Personel Bilgileri
class PersonelListCreateView(generics.ListCreateAPIView):
    queryset = Personel.objects.filter(is_delete=False)
    serializer_class = PersonelSerializer

class PersonelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personel.objects.filter(is_delete=False)
    serializer_class = PersonelSerializer

# Kayıtlar
class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.filter(is_delete=False)
    serializer_class = TourSerializer

class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.filter(is_delete=False)
    serializer_class = TourSerializer

class TransferListCreateView(generics.ListCreateAPIView):
    queryset = Transfer.objects.filter(is_delete=False)
    serializer_class = TransferSerializer

class TransferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.filter(is_delete=False)
    serializer_class = TransferSerializer

class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.filter(is_delete=False)
    serializer_class = VehicleSerializer

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.filter(is_delete=False)
    serializer_class = VehicleSerializer

class GuideListCreateView(generics.ListCreateAPIView):
    queryset = Guide.objects.filter(is_delete=False)
    serializer_class = GuideSerializer

class GuideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guide.objects.filter(is_delete=False)
    serializer_class = GuideSerializer

class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.filter(is_delete=False)
    serializer_class = HotelSerializer

class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.filter(is_delete=False)
    serializer_class = HotelSerializer

class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.filter(is_delete=False)
    serializer_class = ActivitySerializer

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.filter(is_delete=False)
    serializer_class = ActivitySerializer

class MuseumListCreateView(generics.ListCreateAPIView):
    queryset = Museum.objects.filter(is_delete=False)
    serializer_class = MuseumSerializer

class MuseumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Museum.objects.filter(is_delete=False)
    serializer_class = MuseumSerializer

class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.filter(is_delete=False)
    serializer_class = SupplierSerializer

class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.filter(is_delete=False)
    serializer_class = SupplierSerializer

class ActivitysupplierListCreateView(generics.ListCreateAPIView):
    queryset = Activitysupplier.objects.filter(is_delete=False)
    serializer_class = ActivitysupplierSerializer

class ActivitysupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activitysupplier.objects.filter(is_delete=False)
    serializer_class = ActivitysupplierSerializer

class BuyercompanyListCreateView(generics.ListCreateAPIView):
    queryset = Buyercompany.objects.filter(is_delete=False)
    serializer_class = BuyercompanySerializer

class BuyercompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buyercompany.objects.filter(is_delete=False)
    serializer_class = BuyercompanySerializer


#Yönetim
class CostListCreateView(generics.ListCreateAPIView):
    queryset = Cost.objects.filter(is_delete=False)
    serializer_class = CostSerializer

class CostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cost.objects.filter(is_delete=False)
    serializer_class = CostSerializer

class ActivitycostListCreateView(generics.ListCreateAPIView):
    queryset = Activitycost.objects.filter(is_delete=False)
    serializer_class = ActivitycostSerializer

class ActivitycostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activitycost.objects.filter(is_delete=False)
    serializer_class = ActivitycostSerializer


#Operasyon İşlemleri:

#Operasyon

class OperationListCreateView(generics.ListCreateAPIView):
    queryset = Operation.objects.filter(is_delete=False)
    serializer_class = OperationSerializer

class OperationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Operation.objects.filter(is_delete=False)
    serializer_class = OperationSerializer

#Operasyon Gün

class OperationdayListCreateView(generics.ListCreateAPIView):
    queryset = Operationday.objects.filter(is_delete=False)
    serializer_class = OperationdaySerializer

class OperationdayDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Operationday.objects.filter(is_delete=False)
    serializer_class = OperationdaySerializer

#Operation İtem:
class OperationitemListCreateView(generics.ListCreateAPIView):
    queryset = Operationitem.objects.filter(is_delete=False)
    serializer_class = OperationitemSerializer

class OperationitemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Operationitem.objects.filter(is_delete=False)
    serializer_class = OperationitemSerializer


#Şablon kaydetme işlemleri

class OperationTemplateListCreateView(generics.ListCreateAPIView):
    queryset = OperationTemplate.objects.all()
    serializer_class = OperationTemplateSerializer

class OperationTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OperationTemplate.objects.all()
    serializer_class = OperationTemplateSerializer

class OperationdayTemplateListCreateView(generics.ListCreateAPIView):
    queryset = OperationdayTemplate.objects.all()
    serializer_class = OperationdayTemplateSerializer

class OperationdayTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OperationdayTemplate.objects.all()
    serializer_class = OperationdayTemplateSerializer

class OperationitemTemplateListCreateView(generics.ListCreateAPIView):
    queryset = OperationitemTemplate.objects.all()
    serializer_class = OperationitemTemplateSerializer

class OperationitemTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OperationitemTemplate.objects.all()
    serializer_class = OperationitemTemplateSerializer

#Döviz kurları:
class ExchangeRateListCreateView(generics.ListCreateAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

class ExchangeRateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

#Bildirimler

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationReceiptListCreateView(generics.ListCreateAPIView):
    queryset = NotificationReceipt.objects.all()
    serializer_class = NotificationReceiptSerializer

class NotificationReceiptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationReceipt.objects.all()
    serializer_class = NotificationReceiptSerializer

#Destek Kayıtları

class SupportTicketListCreateView(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

class SupportTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

#Sms Gönder:

class SmsgonderListCreateView(generics.ListCreateAPIView):
    queryset = Smsgonder.objects.filter(is_delete=False)
    serializer_class = SmsgonderSerializer

class SmsgonderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Smsgonder.objects.filter(is_delete=False)
    serializer_class = SmsgonderSerializer

#Cari

class CariListCreateView(generics.ListCreateAPIView):
    queryset = Cari.objects.filter(is_delete=False)
    serializer_class = CariSerializer

class CariDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cari.objects.filter(is_delete=False)
    serializer_class = CariSerializer


#Satışlar:

class SellListCreateView(generics.ListCreateAPIView):
    queryset = Sell.objects.filter(is_delete=False)
    serializer_class = SellSerializer

class SellDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sell.objects.filter(is_delete=False)
    serializer_class = SellSerializer


class ActivitysellListCreateView(generics.ListCreateAPIView):
    queryset = Activitysell.objects.filter(is_delete=False)
    serializer_class = ActivitysellSerializer

class ActivitysellDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activitysell.objects.filter(is_delete=False)
    serializer_class = ActivitysellSerializer


#Login İşlemleri
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            return Response({"message": "Login successful", "csrf_token": csrf_token}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Change the password
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({"detail": "Parola başarıyla değiştirildi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

from datetime import date, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta
from .serializers import OperationitemSerializer

class TodayOperationItems(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        items = Operationitem.objects.filter(day__date=date.today(), is_delete=False).order_by('pick_time')
        serializer = OperationitemSerializer(items, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        return response

class TomorrowOperationItems(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tomorrow = date.today() + timedelta(days=1)
        items = Operationitem.objects.filter(day__date=tomorrow, is_delete=False).order_by('pick_time')
        serializer = OperationitemSerializer(items, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        return response

class NextDayOperationItems(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        next_day = date.today() + timedelta(days=2)
        items = Operationitem.objects.filter(day__date=next_day, is_delete=False).order_by('pick_time')
        serializer = OperationitemSerializer(items, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        return response


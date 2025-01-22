from django.contrib.auth.models import User
from rest_framework import serializers
from Core.models import *
# serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



# Sirket
class SirketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sirket
        fields = ['id', 'name', 'start', 'finish', 'is_active', 'statu']



class PersonelSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = SirketSerializer()

    class Meta:
        model = Personel
        fields = ['user', 'company', 'is_active', 'phone', 'job', 'created_at', 'dark_mode']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        personel, created = Personel.objects.update_or_create(user=user, **validated_data)
        return personel

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.company = validated_data.get('company', instance.company)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.job = validated_data.get('job', instance.job)
        instance.dark_mode = validated_data.get('dark_mode', instance.dark_mode)
        instance.save()

        UserSerializer.update(UserSerializer(), instance=user, validated_data=user_data)
        return instance



# Kayıtlar
class TourSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Tour
        fields = ['id', 'company', 'route', 'is_delete']

class TransferSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Transfer
        fields = ['id', 'company', 'route', 'is_delete']

class VehicleSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Vehicle
        fields = ['id', 'company', 'vehicle', 'capacity', 'is_delete']

class GuideSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Guide
        fields = ['id', 'company', 'name', 'city', 'doc_no', 'phone', 'mail', 'price', 'currency', 'is_delete']

class HotelSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Hotel
        fields = ['id', 'company', 'name', 'city', 'mail', 'one_person', 'two_person', 'tree_person', 'finish', 'currency', 'is_delete']

class ActivitySerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Activity
        fields = ['id', 'company', 'name', 'city', 'is_delete']

class MuseumSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Museum
        fields = ['id', 'company', 'name', 'city', 'contact', 'price', 'currency', 'is_delete']

class SupplierSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Supplier
        fields = ['id', 'company', 'name', 'contact', 'is_delete']

class ActivitysupplierSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Activitysupplier
        fields = ['id', 'company', 'name', 'contact', 'is_delete']

class BuyercompanySerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    class Meta:
        model = Buyercompany
        fields = ['id', 'company', 'name', 'short_name', 'contact', 'is_delete']




# Yönetim
class CostSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    supplier = SupplierSerializer()
    tour = TourSerializer()
    transfer = TransferSerializer()

    class Meta:
        model = Cost
        fields = [
            'id', 'company', 'supplier', 'tour', 'transfer', 'car', 'minivan',
            'minibus', 'midibus', 'bus', 'currency', 'is_delete'
        ]

    def validate(self, data):
        if data.get('tour') and data.get('transfer'):
            raise serializers.ValidationError("Tur ve Transfer aynı anda seçilemez.")
        if not data.get('tour') and not data.get('transfer'):
            raise serializers.ValidationError("Tur veya Transfer'den birini seçmelisiniz.")
        return data

class ActivitycostSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    supplier = ActivitysupplierSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = Activitycost
        fields = ['id', 'company', 'supplier', 'activity', 'price', 'currency', 'is_delete']

    def validate(self, data):
        if data.get('price') is None or data.get('price') <= 0:
            raise serializers.ValidationError("Ücret alanı pozitif bir değer olmalıdır.")
        return data


# Operasyon İşlemleri
class OperationSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    selling_staff = PersonelSerializer()
    follow_staff = PersonelSerializer()
    buyer_company = BuyercompanySerializer()

    class Meta:
        model = Operation
        fields = [
            'id', 'company', 'selling_staff', 'follow_staff', 'create_date', 'update_date',
            'buyer_company', 'ticket', 'start', 'finish', 'passenger_info', 'number_passengers',
            'payment_type', 'payment_channel', 'remaining_payment', 'tl_sales_price', 'usd_sales_price',
            'eur_sales_price', 'rbm_sales_price', 'total_sales_price', 'tl_cost_price', 'usd_cost_price',
            'eur_cost_price', 'rbm_cost_price', 'total_cost_price', 'sold', 'tl_activity_price',
            'usd_activity_price', 'eur_activity_price', 'rbm_activity_price', 'is_delete'
        ]

    def validate(self, data):
        if data.get('start') and data.get('finish'):
            if data['start'] > data['finish']:
                raise serializers.ValidationError("Başlama tarihi bitiş tarihinden sonra olamaz.")
        return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

class OperationdaySerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    operation = OperationSerializer()

    class Meta:
        model = Operationday
        fields = ['id', 'company', 'operation', 'date', 'is_delete']

class OperationitemSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    day = OperationdaySerializer()
    tour = TourSerializer()
    transfer = TransferSerializer()
    vehicle = VehicleSerializer()
    supplier = SupplierSerializer()
    cost = CostSerializer()
    hotel = HotelSerializer()
    activity = ActivitySerializer()
    activity_supplier = ActivitysupplierSerializer()
    activity_cost = ActivitycostSerializer()
    new_museum = MuseumSerializer(many=True)
    guide = GuideSerializer()

    class Meta:
        model = Operationitem
        fields = [
            'id', 'company', 'day', 'operation_type', 'pick_time', 'release_time', 'release_location',
            'pick_location', 'tour', 'transfer', 'vehicle', 'supplier', 'manuel_vehicle_price',
            'auto_vehicle_price', 'vehicle_price', 'vehicle_sell_price', 'vehicle_sell_currency',
            'vehicle_currency', 'cost', 'hotel', 'room_type', 'hotel_price', 'hotel_sell_price',
            'hotel_sell_currency', 'hotel_currency', 'hotel_payment', 'activity', 'activity_price',
            'activity_sell_price', 'manuel_activity_price', 'auto_activity_price', 'activity_currency',
            'activity_sell_currency', 'activity_supplier', 'activity_cost', 'activity_payment',
            'new_museum', 'museum_person', 'museum_price', 'museum_sell_price', 'museum_sell_currency',
            'museum_currency', 'museum_payment', 'driver', 'driver_phone', 'plaka', 'guide', 'guide_price',
            'guide_sell_price', 'guide_sell_currency', 'guide_currency', 'guide_var', 'other_price',
            'other_currency', 'other_sell_price', 'other_sell_currency', 'tl_cost_price', 'usd_cost_price',
            'eur_cost_price', 'rmb_cost_price', 'description', 'is_delete', 'is_processed'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['new_museum'] = MuseumSerializer(instance.new_museum.all(), many=True).data
        return representation



# Şablon Kayıtları
class OperationTemplateSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    buyer_company = BuyercompanySerializer()

    class Meta:
        model = OperationTemplate
        fields = ['id', 'company', 'name', 'buyer_company', 'day_numbers', 'tl_sales_price', 'usd_sales_price', 'eur_sales_price', 'rbm_sales_price']

class OperationdayTemplateSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    operation = OperationSerializer()

    class Meta:
        model = OperationdayTemplate
        fields = ['id', 'company', 'operation', 'day_number']

class OperationitemTemplateSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    tour = TourSerializer()
    transfer = TransferSerializer()
    vehicle = VehicleSerializer()
    hotel = HotelSerializer()
    activity = ActivitySerializer()
    new_museum = MuseumSerializer(many=True)

    class Meta:
        model = OperationitemTemplate
        fields = [
            'id', 'company', 'operation', 'operation_type', 'pick_time', 'release_time', 'day', 'tour',
            'transfer', 'vehicle', 'hotel', 'room_type', 'hotel_payment', 'activity', 'activity_payment',
            'new_museum', 'museum_payment', 'description'
        ]

    def create(self, validated_data):
        museums_data = validated_data.pop('new_museum')
        operationitemtemplate = OperationitemTemplate.objects.create(**validated_data)
        operationitemtemplate.new_museum.set(museums_data)
        return operationitemtemplate

    def update(self, instance, validated_data):
        museums_data = validated_data.pop('new_museum')
        instance = super().update(instance, validated_data)
        instance.new_museum.set(museums_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['new_museum'] = MuseumSerializer(instance.new_museum.all(), many=True).data
        return representation


# Döviz Kurları
class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ['id', 'usd_to_try', 'usd_to_eur', 'usd_to_rmb', 'created_at']


# Bildirimler
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'company', 'title', 'message', 'sender', 'recipients_group', 'timestamp']

class NotificationReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationReceipt
        fields = ['id', 'notification', 'recipient', 'read_at']


# Destek Kayıtları
class SupportTicketSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    user = UserSerializer()

    class Meta:
        model = SupportTicket
        fields = ['id', 'company', 'user', 'title', 'description', 'cevap', 'status', 'created_at', 'updated_at']


# Sms Gönder
class SmsgonderSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    user = UserSerializer()

    class Meta:
        model = Smsgonder
        fields = ['id', 'company', 'user', 'staff', 'message', 'created_at', 'updated_at', 'is_delete']
        read_only_fields = ['created_at', 'updated_at']


# Cari
class CariSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    buyer_company = BuyercompanySerializer()
    supplier = SupplierSerializer()
    hotel = HotelSerializer()
    guide = GuideSerializer()
    activity_supplier = ActivitysupplierSerializer()

    class Meta:
        model = Cari
        fields = [
            'id', 'company', 'description', 'transaction_type', 'income', 'expense', 'receipt', 'price',
            'currency', 'buyer_company', 'supplier', 'hotel', 'guide', 'activity_supplier', 'created_staff',
            'create_date', 'update_date', 'is_delete'
        ]
        read_only_fields = ['create_date', 'update_date']


# Satışlar
class SellSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    buyer = BuyercompanySerializer()
    tour = TourSerializer()
    transfer = TransferSerializer()

    class Meta:
        model = Sell
        fields = ['id', 'company', 'buyer', 'tour', 'transfer', 'car', 'minivan', 'minibus', 'midibus', 'bus', 'currency', 'is_delete']

class ActivitysellSerializer(serializers.ModelSerializer):
    company = SirketSerializer()
    buyer = BuyercompanySerializer()
    activity = ActivitySerializer()

    class Meta:
        model = Activitysell
        fields = ['id', 'company', 'buyer', 'activity', 'price', 'currency', 'is_delete']




# Login işlemleri
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("Eski parola yanlış.")
        return value

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise ValidationError("Yeni parola eski parola ile aynı olamaz.")
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        request = self.context.get('request')
        user = User.objects.get(email=self.validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        reset_link = f"{request.scheme}://{request.get_host()}/reset-password/?token={token.key}"
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            token = Token.objects.get(key=data['token'])
        except Token.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        return data

    def save(self):
        token = Token.objects.get(key=self.validated_data['token'])
        user = token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        token.delete()



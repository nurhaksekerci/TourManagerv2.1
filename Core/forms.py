import random
from django import forms
from Core.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class PersonelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Adı")
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Soyadı")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Mail")
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Kullanıcı Adı")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Parola")

    class Meta:
        model = Personel
        fields = ['is_active', 'job', 'phone']
        widgets = {
            'job': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'})  # Doğru widget tanımı
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.user:
            initial = kwargs.get('initial', {})
            initial['first_name'] = instance.user.first_name
            initial['last_name'] = instance.user.last_name
            initial['email'] = instance.user.email
            initial['username'] = instance.user.username
            kwargs['initial'] = initial
        super(PersonelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user_data = {
            'first_name': self.cleaned_data.get('first_name'),
            'last_name': self.cleaned_data.get('last_name'),
            'email': self.cleaned_data.get('email'),
            'username': self.cleaned_data.get('username'),
        }

        personel_is_active = self.cleaned_data.get('is_active')

        if self.instance.pk:
            # Güncelleme
            user = self.instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            if self.cleaned_data.get('password'):
                # Şifre alanı doldurulmuşsa, şifreyi de güncelle
                user.set_password(self.cleaned_data.get('password'))
            # Personel modelindeki is_active alanını User modeline eşitle
            user.is_active = personel_is_active
            user.save()
        else:
            # Yeni Kullanıcı
            user_password = self.cleaned_data.get('password')
            user = User.objects.create_user(**user_data, password=user_password or 'default_password')
            # Personel modelindeki is_active alanını User modeline eşitle
            user.is_active = personel_is_active
            self.instance.user = user

        if commit:
            self.instance.save()
        return self.instance


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle', 'capacity']
        widgets = {
            'vehicle': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['route', 'start_city', 'finish_city']
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'start_city': forms.Select(attrs={'class': 'form-control'}),
            'finish_city': forms.Select(attrs={'class': 'form-control'})
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['route', 'start_city', 'finish_city']
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'start_city': forms.Select(attrs={'class': 'form-control'}),
            'finish_city': forms.Select(attrs={'class': 'form-control'})
        }

class TourRouteForm(forms.ModelForm):
    class Meta:
        model = TourRoute
        fields = ['konum']
        widgets = {
            'konum': forms.Select(attrs={'class': 'form-control'})
        }

class TransferRouteForm(forms.ModelForm):
    class Meta:
        model = TransferRoute
        fields = ['konum']
        widgets = {
            'konum': forms.Select(attrs={'class': 'form-control'})
        }


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['name', 'new_city', 'doc_no', 'phone', 'mail', 'price', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'new_city': forms.Select(attrs={'class': 'form-control'}),
            'doc_no': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'new_city', 'mail', 'one_person', 'two_person', 'tree_person', 'finish', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'new_city': forms.Select(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'one_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'two_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'tree_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'finish': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MuseumForm(forms.ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'new_city', 'contact', 'price', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'new_city': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

class ActivitycostForm(forms.ModelForm):
    class Meta:
        model = Activitycost
        fields = ['supplier', 'activity', 'price', 'currency']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActivitycostForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Activitysupplier.objects.filter(is_delete=False)
        self.fields['activity'].queryset = Activity.objects.filter(is_delete=False)


class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['supplier', 'tour', 'transfer', 'car', 'minivan', 'minibus', 'midibus', 'bus', 'currency']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'tour': forms.Select(attrs={'class': 'form-control'}),
            'transfer': forms.Select(attrs={'class': 'form-control'}),
            'car': forms.NumberInput(attrs={'class': 'form-control'}),
            'minivan': forms.NumberInput(attrs={'class': 'form-control'}),
            'minibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'midibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'bus': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_delete=False)
        self.fields['tour'].queryset = Tour.objects.filter(is_delete=False)
        self.fields['transfer'].queryset = Transfer.objects.filter(is_delete=False)


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ActivitysupplierForm(forms.ModelForm):
    class Meta:
        model = Activitysupplier
        fields = ['name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BuyercompanyForm(forms.ModelForm):
    class Meta:
        model = Buyercompany
        fields = ['name', 'short_name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


SOLD_CHOICES = (
    ('Istendi', 'Istendi'),
    ('Alındı', 'Alındı'),
)

class OperationForm(forms.ModelForm):
    sold = forms.ChoiceField(choices=SOLD_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Operation
        fields = ['follow_staff', 'buyer_company', 'sold', 'ticket', 'start', 'finish', 'usd_sales_price', 'eur_sales_price', 'tl_sales_price', 'rbm_sales_price', 'passenger_info', 'number_passengers', 'payment_channel', 'payment_type', 'usd_activity_price', 'eur_activity_price', 'tl_activity_price', 'rbm_activity_price']
        widgets = {
            'follow_staff': forms.Select(attrs={'class': 'form-control'}),
            'buyer_company': forms.Select(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_channel': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finish': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passenger_info': forms.Textarea(attrs={'class': 'form-control'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'usd_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'eur_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tl_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rbm_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'usd_activity_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'eur_activity_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tl_activity_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rbm_activity_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'number_passengers': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'sold': 'Ödeme Durumu'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OperationForm, self).__init__(*args, **kwargs)
        if self.request:
            personel_instance = self.request.user.personel.first()
            if personel_instance:
                self.fields['follow_staff'].queryset = Personel.objects.filter(company=personel_instance.company)
            else:
                self.fields['follow_staff'].queryset = Personel.objects.none()

            self.fields['buyer_company'].queryset = Buyercompany.objects.filter(company=personel_instance.company, is_delete=False)



class OperationdayForm(forms.ModelForm):
    class Meta:
        model = Operationday
        fields = ['date',]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

from django.utils.crypto import get_random_string

class OperationitemForm(forms.ModelForm):


    class Meta:
        model = Operationitem
        fields = [
            'operation_type', 'pick_time', 'release_time', 'release_location', 'pick_location', 'vehicle_price', 'vehicle_sell_price',
            'tour', 'transfer', 'vehicle', 'supplier', 'manuel_vehicle_price', 'vehicle_currency', 'vehicle_sell_currency', 'museum_person',
            'hotel', 'room_type', 'hotel_price', 'hotel_currency', 'hotel_sell_price', 'hotel_sell_currency',
            'activity', 'activity_price', 'activity_currency', 'activity_supplier', 'manuel_activity_price', 'activity_sell_price', 'activity_sell_currency',
            'new_museum', 'museum_price', 'museum_currency', 'museum_sell_price', 'museum_sell_currency',
            'driver', 'driver_phone', 'plaka', 'guide', 'guide_price', 'guide_currency', 'guide_var', 'guide_sell_price', 'guide_sell_currency',
            'other_price', 'other_currency', 'description', 'activity_payment', 'museum_payment', 'hotel_payment', 'other_sell_price', 'other_sell_currency'
        ]
        widgets = {
            'operation_type': forms.Select(attrs={'class': 'form-control'}),
            'pick_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'release_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'release_location': forms.TextInput(attrs={'class': 'form-control'}),
            'pick_location': forms.TextInput(attrs={'class': 'form-control'}),


            'tour': forms.Select(attrs={'class': 'form-control select'}),
            'transfer': forms.Select(attrs={'class': 'form-control select'}),
            'vehicle': forms.Select(attrs={'class': 'form-control select'}),
            'supplier': forms.Select(attrs={'class': 'form-control select'}),
            'vehicle_currency': forms.Select(attrs={'class': 'form-control select'}),
            'vehicle_sell_currency': forms.Select(attrs={'class': 'form-control select'}),
            'manuel_vehicle_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vehicle_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'vehicle_sell_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'hotel': forms.Select(attrs={'class': 'form-control select'}),
            'room_type': forms.Select(attrs={'class': 'form-control select'}),
            'hotel_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotel_currency': forms.Select(attrs={'class': 'form-control'}),
            'hotel_sell_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotel_sell_currency': forms.Select(attrs={'class': 'form-control'}),
            'hotel_payment' : forms.Select(attrs={'class': 'form-control'}),

            'activity': forms.Select(attrs={'class': 'form-control select'}),
            'activity_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'activity_sell_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'manuel_activity_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_currency': forms.Select(attrs={'class': 'form-control'}),
            'activity_sell_currency': forms.Select(attrs={'class': 'form-control'}),
            'activity_supplier': forms.Select(attrs={'class': 'form-control select'}),
            'activity_payment' : forms.Select(attrs={'class': 'form-control'}),

            'new_museum': forms.SelectMultiple(attrs={'class': 'form-control selectmulti'}),
            'museum_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'museum_sell_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'museum_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'museum_currency': forms.Select(attrs={'class': 'form-control'}),
            'museum_sell_currency': forms.Select(attrs={'class': 'form-control'}),
            'museum_payment' : forms.Select(attrs={'class': 'form-control'}),

            'driver': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'plaka': forms.TextInput(attrs={'class': 'form-control'}),
            'guide': forms.Select(attrs={'class': 'form-control select'}),
            'guide_var': forms.Select(attrs={'class': 'form-control'}),
            'guide_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'guide_currency': forms.Select(attrs={'class': 'form-control'}),
            'other_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_currency': forms.Select(attrs={'class': 'form-control'}),
            'guide_sell_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'guide_sell_currency': forms.Select(attrs={'class': 'form-control'}),
            'other_sell_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_sell_currency': forms.Select(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super(OperationitemForm, self).__init__(*args, **kwargs)
        # Querysetleri optimize etmek için order_by() kullanımı
        self.fields['guide'].queryset = Guide.objects.order_by('name')
        self.fields['activity'].queryset = Activity.objects.order_by('name')
        self.fields['tour'].queryset = Tour.objects.order_by('route')
        self.fields['transfer'].queryset = Transfer.objects.order_by('route')
        self.fields['new_museum'].queryset = Museum.objects.order_by('city')
        self.fields['hotel'].queryset = Hotel.objects.order_by('name')
        self.fields['supplier'].queryset = Supplier.objects.order_by('name')
        self.fields['activity_supplier'].queryset = Activitysupplier.objects.order_by('name')
        # Diğer Select alanları için benzer sıralamalar yapılabilir


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(OperationitemForm, self).__init__(*args, **kwargs)
        if request and 'new_museum' in self.fields:
            user_company = request.user.personel.first().company
            self.fields['new_museum'].queryset = Museum.objects.filter(company=user_company, is_delete=False)
            self.fields['activity'].queryset = Activity.objects.filter(company=user_company, is_delete=False)
            self.fields['guide'].queryset = Guide.objects.filter(company=user_company, is_delete=False)
            self.fields['tour'].queryset = Tour.objects.filter(company=user_company, is_delete=False)
            self.fields['transfer'].queryset = Transfer.objects.filter(company=user_company, is_delete=False)
            self.fields['supplier'].queryset = Supplier.objects.filter(company=user_company, is_delete=False)
            self.fields['activity_supplier'].queryset = Activitysupplier.objects.filter(company=user_company, is_delete=False)





class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'recipients_group']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recipients_group': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Başlık',
            'message': 'Mesaj',
            'recipients_group': 'Alıcı Grubu'
        }
        help_texts = {
            'title': 'Bildirimin başlığını giriniz.',
            'message': 'Bildirim mesajınızı giriniz.',
            'recipients_group': 'Bu bildirimi kimlerin alacağını seçiniz.'
        }



class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'description']
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Başlık',
            'description': 'Açıklama',
        }


class SupportTicketCevapForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['cevap', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cevap': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': 'Durum',
            'cevap': 'Cevap',
        }


class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = ['buyer', 'tour', 'transfer', 'car', 'minivan', 'minibus', 'midibus', 'bus', 'currency']
        widgets = {
            'buyer': forms.Select(attrs={'class': 'form-control'}),
            'tour': forms.Select(attrs={'class': 'form-control'}),
            'transfer': forms.Select(attrs={'class': 'form-control'}),
            'car': forms.NumberInput(attrs={'class': 'form-control'}),
            'minivan': forms.NumberInput(attrs={'class': 'form-control'}),
            'minibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'midibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'bus': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }


class ActivitysellForm(forms.ModelForm):
    class Meta:
        model = Activitysell
        fields = ['buyer', 'activity', 'price', 'currency']
        widgets = {
            'buyer': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

class SmsgonderForm(forms.ModelForm):
    class Meta:
        model = Smsgonder
        fields = ['staff', 'message']
        widgets = {
            'staff': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SmsgonderForm, self).__init__(*args, **kwargs)
        if self.request:
            personel_instance = self.request.user.personel.first()
            if personel_instance:
                self.fields['staff'].queryset = Personel.objects.filter(company=personel_instance.company)
            else:
                self.fields['staff'].queryset = Personel.objects.none()


class CariForm(forms.ModelForm):
    class Meta:
        model = Cari
        fields = [
            'transaction_type',
            'income',
            'expense',
            'receipt',
            'price',
            'description',
            'currency',
            'buyer_company',
            'supplier',
            'activity_supplier',
            'hotel',
            'guide',
        ]
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'buyer_company': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'activity_supplier': forms.Select(attrs={'class': 'form-control'}),
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'guide': forms.Select(attrs={'class': 'form-control'}),
            'income': forms.Select(attrs={'class': 'form-control'}),
            'expense': forms.Select(attrs={'class': 'form-control'}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CariForm, self).__init__(*args, **kwargs)
        if self.request:
            personel = Personel.objects.get(user=self.request.user)
            company = personel.company
            self.fields['buyer_company'].queryset = Buyercompany.objects.filter(company=company)
            self.fields['supplier'].queryset = Supplier.objects.filter(company=company)
            self.fields['activity_supplier'].queryset = Activitysupplier.objects.filter(company=company)
            self.fields['hotel'].queryset = Hotel.objects.filter(company=company)
            self.fields['guide'].queryset = Guide.objects.filter(company=company)

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        income = cleaned_data.get('income')
        expense = cleaned_data.get('expense')

        if transaction_type == 'income' and not income:
            self.add_error('income', 'Gelir kaynağını belirtmelisiniz.')
        elif transaction_type == 'expense' and not expense:
            self.add_error('expense', 'Gider kaynağını belirtmelisiniz.')

        return cleaned_data


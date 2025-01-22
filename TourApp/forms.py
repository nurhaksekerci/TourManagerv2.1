from django import forms
from Core.models import (
    Tour, Transfer, Vehicle, Guide, Hotel, Activity, Museum, Vehiclecost,
    Supplier, VehiclesupplierCities, Activitysupplier,
    ActivitysupplierCities, Tourvehiclecost, Transfervehiclecost,
    Activitycost, Buyercompany, Operationitem
)
from django import forms
from django.contrib.auth.models import User
from Core.models import Personel

class CustomSelectWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'form-control', 'data-select2-selector': 'status'})

class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'form-control'})

class CustomNumberInput(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'form-control'})

class CustomCheckboxInput(forms.CheckboxInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'form-check-input'})


class PersonelForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=CustomTextInput(), label="Kullanıcı Adı")
    first_name = forms.CharField(max_length=30, widget=CustomTextInput(), label="Ad")
    last_name = forms.CharField(max_length=30, widget=CustomTextInput(), label="Soyad")
    email = forms.EmailField(widget=CustomTextInput(), label="E-posta")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Şifre", required=False)

    class Meta:
        model = Personel
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone', 'job', 'gender']
        widgets = {
            'is_active': CustomCheckboxInput(),
            'phone': CustomTextInput(),
            'job': CustomSelectWidget(),
            'gender': CustomSelectWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(PersonelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Güncelleme durumu
            self.fields.pop('password')
        else:
            # Oluşturma durumu
            self.fields['password'].required = True

    def save(self, commit=True):
        # User oluşturma veya güncelleme kısmı
        user_data = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
        }
        user = self.instance.user if self.instance.pk else User(**user_data)

        if 'password' in self.cleaned_data and self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        # Personel kaydetme kısmı
        employee = super(PersonelForm, self).save(commit=False)
        employee.user = user

        if commit:
            employee.save()

        return employee



class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['route', 'start_city', 'finish_city']
        widgets = {
            'route': CustomTextInput(),
            'start_city': CustomSelectWidget(),
            'finish_city': CustomSelectWidget(),
        }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['route', 'start_city', 'finish_city']
        widgets = {
            'route': CustomTextInput(),
            'start_city': CustomSelectWidget(),
            'finish_city': CustomSelectWidget(),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle', 'capacity']
        widgets = {
            'vehicle': CustomTextInput(),
            'capacity': CustomNumberInput(),
        }

class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['name', 'new_city', 'doc_no', 'phone', 'mail', 'price', 'currency']
        widgets = {
            'name': CustomTextInput(),
            'new_city': CustomSelectWidget(),
            'doc_no': CustomTextInput(),
            'phone': CustomTextInput(),
            'mail': CustomTextInput(),
            'price': CustomNumberInput(),
            'currency': CustomSelectWidget(),
        }

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'new_city', 'finish', 'mail', 'one_person', 'two_person', 'tree_person', 'currency']
        widgets = {
            'name': CustomTextInput(),
            'new_city': CustomSelectWidget(),
            'finish': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mail': CustomTextInput(),
            'one_person': CustomNumberInput(),
            'two_person': CustomNumberInput(),
            'tree_person': CustomNumberInput(),
            'currency': CustomSelectWidget(),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name']
        widgets = {
            'name': CustomTextInput(),
        }

class MuseumForm(forms.ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'contact', 'price', 'currency', 'new_city']
        widgets = {
            'name': CustomTextInput(),
            'contact': CustomTextInput(),
            'price': CustomNumberInput(),
            'currency': CustomSelectWidget(),
            'new_city': CustomSelectWidget(),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact']
        widgets = {
            'name': CustomTextInput(),
            'contact': CustomTextInput(),
        }

class VehiclesupplierCitiesForm(forms.ModelForm):
    class Meta:
        model = VehiclesupplierCities
        fields = ['supplier', 'city']
        widgets = {
            'supplier': CustomSelectWidget(),
            'city': CustomSelectWidget(),
        }

class ActivitysupplierForm(forms.ModelForm):
    class Meta:
        model = Activitysupplier
        fields = ['name', 'contact']
        widgets = {
            'name': CustomTextInput(),
            'contact': CustomTextInput(),
        }

class ActivitysupplierCitiesForm(forms.ModelForm):
    class Meta:
        model = ActivitysupplierCities
        fields = ['supplier', 'city']
        widgets = {
            'supplier': CustomSelectWidget(),
            'city': CustomSelectWidget(),
        }

class ActivitycostForm(forms.ModelForm):
    class Meta:
        model = Activitycost
        fields = ['supplier', 'activity', 'price', 'currency']
        widgets = {
            'supplier': CustomSelectWidget(),
            'activity': CustomSelectWidget(),
            'price': CustomNumberInput(),
            'currency': CustomSelectWidget(),
        }

class BuyercompanyForm(forms.ModelForm):
    class Meta:
        model = Buyercompany
        fields = ['name', 'short_name', 'contact']
        widgets = {
            'name': CustomTextInput(),
            'short_name': CustomTextInput(),
            'contact': CustomTextInput(),
        }



class ActivitysupplierCitiesForm(forms.ModelForm):
    class Meta:
        model = ActivitysupplierCities
        fields = ['city',]
        widgets = {
            'city': CustomSelectWidget(),
        }

class VehiclesupplierCitiesForm(forms.ModelForm):
    class Meta:
        model = VehiclesupplierCities
        fields = ['city',]
        widgets = {
            'city': CustomSelectWidget(),
        }

class VehiclecostForm(forms.ModelForm):
    class Meta:
        model = Vehiclecost
        fields = ['vehicle', 'price', 'currency']
        widgets = {
            'vehicle': CustomSelectWidget(),
            'price': CustomNumberInput(),
            'currency': CustomSelectWidget(),
        }


class TourvehiclecostForm(forms.ModelForm):
    class Meta:
        model = Tourvehiclecost
        fields = ['tour', 'vehicle_cost', 'supplier']
        widgets = {
            'tour': CustomSelectWidget(),
            'vehicle_cost': CustomSelectWidget(),
            'supplier': CustomSelectWidget(),
        }

class TransfervehiclecostForm(forms.ModelForm):
    class Meta:
        model = Transfervehiclecost
        fields = ['transfer', 'vehicle_cost', 'supplier']
        widgets = {
            'transfer': CustomSelectWidget(),
            'vehicle_cost': CustomSelectWidget(),
            'supplier': CustomSelectWidget(),
        }

class OperationitemCreateForm(forms.ModelForm):
    class Meta:
        model = Operationitem
        fields = [
            'operation_type', 'pick_time', 'release_location', 'pick_location',
            'tour', 'transfer', 'vehicle',
            'hotel', 'room_type', 'hotel_sell_price', 'hotel_sell_currency',
            'activity', 'activity_sell_price', 'activity_sell_currency', 'activity_payment',
            'new_museum', 'museum_sell_price', 'museum_sell_currency', 'museum_payment',
            'driver', 'driver_phone', 'plaka',
            'guide', 'guide_sell_price', 'guide_sell_currency', 'guide_var',
            'other_sell_price', 'other_sell_currency',
            'description'
        ]
        widgets = {
            'operation_type': CustomSelectWidget(),
            'pick_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'release_location': CustomTextInput(),
            'pick_location': CustomTextInput(),
            'tour': CustomSelectWidget(),
            'transfer': CustomSelectWidget(),
            'vehicle': CustomSelectWidget(),
            'vehicle_sell_price': CustomNumberInput(),
            'vehicle_sell_currency': CustomSelectWidget(),
            'hotel': CustomSelectWidget(),
            'room_type': CustomSelectWidget(),
            'hotel_sell_price': CustomNumberInput(),
            'hotel_sell_currency': CustomSelectWidget(),
            'hotel_payment': CustomSelectWidget(),
            'activity': CustomSelectWidget(),
            'activity_sell_price': CustomNumberInput(),
            'activity_sell_currency': CustomSelectWidget(),
            'activity_payment': CustomSelectWidget(),
            'new_museum': forms.SelectMultiple(attrs={'class': 'form-control', 'data-select2-selector': 'museum'}),
            'museum_sell_price': CustomNumberInput(),
            'museum_sell_currency': CustomSelectWidget(),
            'museum_payment': CustomSelectWidget(),
            'driver': CustomTextInput(),
            'driver_phone': CustomTextInput(),
            'plaka': CustomTextInput(),
            'guide': CustomSelectWidget(),
            'guide_sell_price': CustomNumberInput(),
            'guide_sell_currency': CustomSelectWidget(),
            'guide_var': CustomSelectWidget(),
            'other_sell_price': CustomNumberInput(),
            'other_sell_currency': CustomSelectWidget(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }



class OperationitemForm(forms.ModelForm):
    class Meta:
        model = Operationitem
        fields = [
            'operation_type', 'pick_time', 'release_location', 'pick_location',
            'tour', 'transfer', 'vehicle', 'supplier', 'manuel_vehicle_price',
            'vehicle_sell_price', 'vehicle_sell_currency', 'vehicle_currency',
            'cost', 'hotel', 'room_type', 'hotel_price',
            'hotel_sell_price', 'hotel_sell_currency', 'hotel_currency',
            'hotel_payment', 'activity', 'activity_sell_price', 'manuel_activity_price',
            'activity_currency', 'activity_sell_currency', 'activity_supplier',
            'activity_cost', 'activity_payment', 'new_museum',
            'museum_price', 'museum_sell_price', 'museum_sell_currency', 'museum_currency',
            'museum_payment', 'driver', 'driver_phone', 'plaka', 'guide', 'guide_price',
            'guide_sell_price', 'guide_sell_currency', 'guide_currency', 'guide_var',
            'other_price', 'other_currency', 'other_sell_price', 'other_sell_currency',
            'description'
        ]
        widgets = {
            'operation_type': CustomSelectWidget(),
            'pick_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'release_location': CustomTextInput(),
            'pick_location': CustomTextInput(),
            'tour': CustomSelectWidget(),
            'transfer': CustomSelectWidget(),
            'vehicle': CustomSelectWidget(),
            'supplier': CustomSelectWidget(),
            'manuel_vehicle_price': CustomNumberInput(),
            'vehicle_sell_price': CustomNumberInput(),
            'vehicle_sell_currency': CustomSelectWidget(),
            'vehicle_currency': CustomSelectWidget(),
            'tour_cost': CustomSelectWidget(),
            'transfer_cost': CustomSelectWidget(),
            'hotel': CustomSelectWidget(),
            'room_type': CustomSelectWidget(),
            'hotel_price': CustomNumberInput(),
            'hotel_sell_price': CustomNumberInput(),
            'hotel_sell_currency': CustomSelectWidget(),
            'hotel_currency': CustomSelectWidget(),
            'hotel_payment': CustomSelectWidget(),
            'activity': CustomSelectWidget(),
            'activity_sell_price': CustomNumberInput(),
            'manuel_activity_price': CustomNumberInput(),
            'activity_currency': CustomSelectWidget(),
            'activity_sell_currency': CustomSelectWidget(),
            'activity_supplier': CustomSelectWidget(),
            'activity_cost': CustomSelectWidget(),
            'activity_payment': CustomSelectWidget(),
            'new_museum': forms.SelectMultiple(attrs={'class': 'form-control', 'data-select2-selector': 'museum'}),
            'museum_price': CustomNumberInput(),
            'museum_sell_price': CustomNumberInput(),
            'museum_sell_currency': CustomSelectWidget(),
            'museum_currency': CustomSelectWidget(),
            'museum_payment': CustomSelectWidget(),
            'driver': CustomTextInput(),
            'driver_phone': CustomTextInput(),
            'plaka': CustomTextInput(),
            'guide': CustomSelectWidget(),
            'guide_price': CustomNumberInput(),
            'guide_sell_price': CustomNumberInput(),
            'guide_sell_currency': CustomSelectWidget(),
            'guide_currency': CustomSelectWidget(),
            'guide_var': CustomSelectWidget(),
            'other_price': CustomNumberInput(),
            'other_currency': CustomSelectWidget(),
            'other_sell_price': CustomNumberInput(),
            'other_sell_currency': CustomSelectWidget(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ActivitysupplierCitiesForm(forms.ModelForm):
    class Meta:
        model = ActivitysupplierCities
        fields = ['city',]  # Formda yer alacak alanlar
        widgets = {
            'city': CustomSelectWidget(),  # city alanı için özel select widget'ı kullanılıyor
        }


class VehiclesupplierCitiesForm(forms.ModelForm):
    class Meta:
        model = VehiclesupplierCities
        fields = ['city',]  # Formda yer alacak alanlar
        widgets = {
            'city': CustomSelectWidget(),  # city alanı için özel select widget'ı kullanılıyor
        }

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Subquery
from sklad.models import *


class NomenklatureAddForm(forms.ModelForm):
    class Meta:
        model = Nomenclature
        fields = '__all__'


class BuyerAddForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'


class VendorAddForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'fio', 'email', 'phone', 'categories']

#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['bank_details'].queryset = BankDetails.objects.exclude(
#            pk__in=Subquery(Vendor.objects.values('bank_details')))


class BankDetailsAddForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ['account', 'bank_name']


class DeliveryAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['vendor', 'nomenclatures']


class ShipmentAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['buyer', 'nomenclatures']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

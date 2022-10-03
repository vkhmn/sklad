from django import forms
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
        fields = ['name', 'address', 'bank_details', 'fio', 'email', 'phone', 'category']


class DeliveryAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['vendor', 'nomenclatures']


class ShipmentAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['buyer', 'nomenclatures']

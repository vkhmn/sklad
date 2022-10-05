from django import forms
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
        fields = ['name', 'address', 'bank_details', 'fio', 'email', 'phone', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_details'].queryset = BankDetails.objects.exclude(
            pk__in=Subquery(Vendor.objects.values('bank_details')))


class DeliveryAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['vendor', 'nomenclatures']


class ShipmentAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['buyer', 'nomenclatures']

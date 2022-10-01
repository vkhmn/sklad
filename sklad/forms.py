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
        fields = '__all__'


class DeliveryAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class ShipmentAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

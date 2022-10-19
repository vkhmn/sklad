from django import forms

from .models import Buyer, Vendor, BankDetails


class BuyerAddForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['fio', 'email', 'phone']
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VendorAddForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'fio', 'email', 'phone', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class BankDetailsAddForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ['account', 'bank_name']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.NumberInput(attrs={'class': 'form-control'}),
        }

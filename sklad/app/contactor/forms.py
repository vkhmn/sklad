from dal import autocomplete
from django import forms

from app.contactor.models import Vendor, BankDetails, Person


class PersonAddForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['full_name', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VendorAddForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': autocomplete.ModelSelect2Multiple(
                'autocomplete_category', attrs={'class': 'form-control'}
            ),
        }


class BankDetailsAddForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ['account', 'bank_name']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.NumberInput(attrs={'class': 'form-control'}),
        }

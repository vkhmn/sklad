from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory

from sklad.models import *


class NomenklatureAddForm(forms.ModelForm):
    class Meta:
        model = Nomenclature
        fields = ['name', 'article', 'price', 'subcategory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
        }


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


class DeliveryAddForm(forms.Form):
    contactor = forms.ModelChoiceField(
        queryset=Vendor.objects.all(),
        label='Поставщик',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )


class ShipmentAddForm(forms.Form):
    contactor = forms.ModelChoiceField(
        queryset=Buyer.objects.all(),
        label='Покупатель',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )


class DocumentNomenclaturesAddForm(forms.Form):
    nomenclature = forms.ModelChoiceField(
        queryset=Nomenclature.objects.all(),
        label='Номенклатура',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    amount = forms.IntegerField(
        initial=1,
        min_value=1,
        label='Количество',
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )


DocumentNomenclaturesFormSet = formset_factory(
    DocumentNomenclaturesAddForm
)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

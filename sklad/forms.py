from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Subquery
from django.forms import modelformset_factory, formset_factory

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


class DeliveryAddForm(forms.Form):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.all()
    )

    # nomenclatures = forms.ModelMultipleChoiceField(
    #    queryset=Nomenclature.objects.all(),
    #    widget=forms.CheckboxSelectMultiple()
    # )


class DocumentNomenclaturesAddForm(forms.Form):
    nomenclature = forms.ModelChoiceField(
        queryset=Nomenclature.objects.all(),
    )
    amount = forms.IntegerField(initial=1, min_value=1)


DocumentNomenclaturesFormSet = formset_factory(
    DocumentNomenclaturesAddForm
)


class ShipmentAddForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['buyer', 'nomenclatures']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

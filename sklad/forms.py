from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory

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
        queryset=Vendor.objects.all(),
        label='Поставщик'

    )

    # nomenclatures = forms.ModelMultipleChoiceField(
    #    queryset=Nomenclature.objects.all(),
    #    widget=forms.CheckboxSelectMultiple()
    # )


class ShipmentAddForm(forms.Form):
    buyer = forms.ModelChoiceField(
        queryset=Buyer.objects.all(),
        label='Покупатель'

    )


class DocumentNomenclaturesAddForm(forms.Form):
    nomenclature = forms.ModelChoiceField(
        queryset=Nomenclature.objects.all(),
        label='Номенклатура'
    )
    amount = forms.IntegerField(
        initial=1,
        min_value=1,
        label='Количество'
    )


DocumentNomenclaturesFormSet = formset_factory(
    DocumentNomenclaturesAddForm
)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

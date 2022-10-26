from django import forms
from django.forms import formset_factory

from app.contactor.models import Vendor, Buyer
from app.nomenclature.models import Nomenclature


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
        queryset=Buyer.objects.select_related('person'),
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

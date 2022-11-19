from dal import autocomplete
from django import forms

from app.nomenclature.models import Nomenclature


class NomenclatureAddForm(forms.ModelForm):
    class Meta:
        model = Nomenclature
        fields = ['name', 'article', 'price', 'subcategory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'subcategory':  autocomplete.ModelSelect2(
                'autocomplete_subcategory', attrs={'class': 'form-control'}
            ),
        }

from django import forms

from app.nomenclature.models import Nomenclature


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

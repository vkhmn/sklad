from django import forms
from sklad.models import *


class AddNomenklatureForm(forms.ModelForm):
    class Meta:
        model = Nomenclature
        fields = '__all__'
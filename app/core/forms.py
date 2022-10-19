from django import forms
from django.contrib.auth.forms import AuthenticationForm


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


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Поиск',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

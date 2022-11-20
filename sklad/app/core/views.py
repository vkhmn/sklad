from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from app.core.forms import LoginUserForm


class LoginUser(LoginView):
    """Представление для авторизации пользователя."""

    form_class = LoginUserForm
    template_name = 'core/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Авторизация'
        )
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """Представление для выхода пользователя."""

    logout(request)
    return redirect('login')

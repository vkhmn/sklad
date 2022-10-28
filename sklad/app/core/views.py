from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse

from app.core.forms import LoginUserForm
from app.core.mixin import DataMixin
from app.nomenclature.models import Nomenclature


class LoginUser(DataMixin, LoginView):
    """Представление для авторизации пользователя."""

    form_class = LoginUserForm
    template_name = 'core/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Авторизация'
            )
        )
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """Представление для выхода пользователя."""

    logout(request)
    return redirect('login')


# For Ajax TEST
def ajax_view(request):
    context = {}
    return render(request, 'core/ajax.html', context=context)


def search_result(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = None
        series = request.POST.get('series')
        query_se = Nomenclature.objects.filter(name__icontains=series)
        print('Is AJAX')
        if len(query_se) > 0 and len(series) > 0:
            data = []
            for pos in query_se:
                item = {
                    'url': pos.get_absolute_url(),
                    'name': pos.name,
                }
                data.append(item)
            res = data
        else:
            res = 'No Nomenclature found'
        print(res)
        return JsonResponse({'data': res})
    print({}, request.headers)
    return JsonResponse({})

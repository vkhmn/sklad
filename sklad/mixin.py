from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from sklad.models import *


menu = [
    {'url_name': 'vendor_list', 'title': 'Поставщики'},
    {'url_name': 'buyer_list', 'title': 'Покупатели'},
    {'url_name': 'nomenclature_list', 'title': 'Номеклатура'},
    {'url_name': 'delivery_list', 'title': 'Поставка'},
    {'url_name': 'shipment_list', 'title': 'Отгрузка'},
]


class SuperUserRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is superuser."""
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_superuser:
            context['menu'] = menu
        return context

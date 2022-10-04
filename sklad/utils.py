from sklad.models import *
from django.db.models import Count


menu = [
    {'url_name': 'vendor_list', 'title': 'Поставщики'},
    {'url_name': 'buyer_list', 'title': 'Покупатели'},
    {'url_name': 'nomenclature_list', 'title': 'Номеклатура'},
    {'url_name': 'delivery_list', 'title': 'Поставка'},
    {'url_name': 'shipment_list', 'title': 'Отгрузка'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

from sklad.models import *
from django.db.models import Count


menu = [
    {'url_name': 'home', 'title': 'Поставщики'},
    {'url_name': 'home', 'title': 'Покупатели'},
    {'url_name': 'nomenclature_list', 'title': 'Номеклатура'},
    {'url_name': 'home', 'title': 'Поставка'},
    {'url_name': 'home', 'title': 'Отгрузка'},
    {'url_name': 'home', 'title': 'Операции'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['subcats'] = SubCategory.objects.annotate(Count('nomenclature')).order_by('name')
        context['cats'] = Category.objects.annotate(Count('subcategory__nomenclature')).order_by('name')

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        if 'subcat_selected' not in context:
            context['subcat_selected'] = 0

        return context

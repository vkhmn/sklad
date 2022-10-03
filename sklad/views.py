from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from sklad.models import *
from sklad.utils import DataMixin
from sklad.forms import *


class IndexView(DataMixin, ListView):
    """"Веб сервис отображающий главную страницу, с последними заявками на
    отгрузку (поставку) товара."""

    model = Document
    template_name = 'sklad/index.html'
    context_object_name = 'documents'
    extra_context = {'title': 'Заявки на поставку/отгрузку'}
    ordering = ['-time_create']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class DeliveryListView(IndexView):
    """"Веб сервис для работы с заявками на поставку."""
    extra_context = {
        'left_menu': [
            {'url_name': 'delivery_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на поставку',
    }

    def get_queryset(self):
        return Document.objects.filter(vendor__isnull=False).order_by('-time_create')


class ShipmentListView(IndexView):
    """"Веб сервис для работы с заявками."""
    extra_context = {
        'left_menu': [
            {'url_name': 'shipment_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на отгрузку',
    }

    def get_queryset(self):
        return Document.objects.filter(buyer__isnull=False).order_by('-time_create')


class DocumentView(DataMixin, DetailView):
    """" Веб сервис для работы с заявкой
    на поставку/отгрузку (отображение карточки) """

    model = Document
    template_name = 'sklad/document.html'
    context_object_name = 'document'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация по заявке")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class NomenclatureListView(DataMixin, ListView):
    """"Веб сервис для работы с номенклатурой
    (отображение, поиск, добавление)."""

    model = Nomenclature
    template_name = 'sklad/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class BuyerListView(DataMixin, ListView):
    """"Веб сервис для работы с покупателями"""

    model = Buyer
    template_name = 'sklad/contactor_list.html'
    context_object_name = 'buyers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'buyer_add', 'title': 'Создать покупателя'}
        ]
        context['title'] = 'Покупатели'
        return context


class VendorListView(DataMixin, ListView):
    """"Веб сервис для работы с поставщиками"""

    model = Vendor
    template_name = 'sklad/contactor_list.html'
    context_object_name = 'vendors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        context['title'] = 'Поставщики'
        return context


class CategoryView(DataMixin, ListView):
    """"Веб сервис для работы с номенклатурой
    (отображение, фильтрация) в зависимости от выбранной категории."""

    model = Nomenclature
    template_name = 'sklad/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Nomenclature.objects.filter(subcategory__category=self.kwargs['pk'])


class SubCategoryView(CategoryView, ListView):
    """"Веб сервис для работы с номенклатурой
      (отображение, фильтрация) в зависимости от выбранной подкатегории."""

    def get_queryset(self):
        return Nomenclature.objects.filter(subcategory=self.kwargs['pk'])


class NomenclatureView(DataMixin, DetailView):
    """"Веб сервис для работы с номенклатурой
      (отображение карточки)"""

    model = Nomenclature
    template_name = 'sklad/nomenclature.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class BuyerView(DataMixin, DetailView):
    """"Веб сервис для работы с покупателем
      (отображение карточки)"""

    model = Buyer
    template_name = 'sklad/details_contactor.html'
    context_object_name = 'buyer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Сведения о покупателе")
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'buyer_add', 'title': 'Создать покупателя'}
        ]
        return context


class VendorView(DataMixin, DetailView):
    """"Веб сервис для работы с покупателем
      (отображение карточки)"""

    model = Vendor
    template_name = 'sklad/details_contactor.html'
    context_object_name = 'vendor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Сведения о поставщике")
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        return context


class NomenklatureAddView(DataMixin, CreateView):
    """"Веб сервис для добавления номенклатуры. """

    form_class = NomenklatureAddForm
    template_name = 'sklad/nomenclature_add.html'
    success_url = reverse_lazy('nomenclature_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление номенклатуры')
        return dict(list(context.items()) + list(c_def.items()))


class BuyerAddView(DataMixin, CreateView):
    """"Веб сервис для добавления покупателя. """

    form_class = BuyerAddForm
    template_name = 'sklad/contactor_add.html'
    success_url = reverse_lazy('buyer_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление покупателя')
        context['left_menu'] = [
            {'url_name': 'buyer_add', 'title': 'Создать покупателя'}
        ]
        return dict(list(context.items()) + list(c_def.items()))


class VendorAddView(DataMixin, CreateView):
    """"Веб сервис для добавления поставщика. """

    form_class = VendorAddForm
    template_name = 'sklad/contactor_add.html'
    success_url = reverse_lazy('vendor_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление поставщика')
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        return dict(list(context.items()) + list(c_def.items()))


class ShipmentAddView(DataMixin, CreateView):
    """"Веб сервис для создания заявки на отгрузку. """

    form_class = ShipmentAddForm
    template_name = 'sklad/shipment_add.html'
    success_url = reverse_lazy('shipment_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание заявки на отгрузку')
        return dict(list(context.items()) + list(c_def.items()))


class DeliveryAddView(DataMixin, CreateView):
    """"Веб сервис для создания заявки на поставку. """

    form_class = DeliveryAddForm
    template_name = 'sklad/delivery_add.html'
    success_url = reverse_lazy('delivery_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание заяки на поставку')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterView(ListView):
    model = Nomenclature
    template_name = 'sklad/register.html'


class LoginView(ListView):
    model = Nomenclature
    template_name = 'sklad/login.html'


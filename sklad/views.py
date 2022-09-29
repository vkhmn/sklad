from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from sklad.models import *
from sklad.utils import DataMixin
from sklad.forms import AddNomenklatureForm


class IndexView(DataMixin, ListView):
    """"Веб сервис отображающий главную страницу, с последними заявками на
    отгрузку (поставку) товара."""

    model = Delivery
    template_name = 'sklad/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
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

    def get_queryset(self):
        return Nomenclature.objects.all()


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

    def get_queryset(self):
        return Nomenclature.objects.filter(pk=self.kwargs['pk'])


class NomenklatureAddView(DataMixin, CreateView):
    """"Веб сервис для добавления номенклатуры. """

    form_class = AddNomenklatureForm
    template_name = 'sklad/nomenclature_add.html'
    success_url = reverse_lazy('nomenclature_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление номенклатуры')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterView(ListView):
    model = Nomenclature
    template_name = 'sklad/register.html'


class LoginView(ListView):
    model = Nomenclature
    template_name = 'sklad/login.html'


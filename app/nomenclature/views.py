from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Count, Sum, F, Q

from app.core.mixin import SuperUserRequiredMixin, DataMixin
from app.core.forms import SearchForm
from .forms import NomenklatureAddForm
from .models import Nomenclature, SubCategory, Category, Store


class NomenclatureListView(SuperUserRequiredMixin, DataMixin, ListView):
    """"Веб сервис для работы с номенклатурой
    (отображение, поиск, добавление)."""

    model = Nomenclature
    template_name = 'nomenclature/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Номенклатура")
        context = dict(list(context.items()) + list(c_def.items()))
        context['subcats'] = SubCategory.objects.annotate(total=Count(
            'nomenclature')
        ).filter(total__gt=0).order_by('category__name', 'name')
        context['search_form'] = SearchForm(data=self.request.GET)
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Nomenclature.objects.filter(name__icontains=query).annotate(
            store_amount=F('store__amount')).order_by(
            'subcategory__category__name',
            'subcategory__name',
            'name'
        )


class CategoryBase(SuperUserRequiredMixin, DataMixin, ListView):
    model = Nomenclature
    template_name = 'nomenclature/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        context['subcats'] = SubCategory.objects.annotate(total=Count(
            'nomenclature')
        ).filter(total__gt=0).order_by('category__name', 'name')
        context['search_form'] = SearchForm(data=self.request.GET)
        return context


class CategoryView(CategoryBase):
    """"Веб сервис для работы с номенклатурой
    (отображение, фильтрация) в зависимости от выбранной категории."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk']).name
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Nomenclature.objects.filter(
            subcategory__category=self.kwargs['pk']
        ).filter(name__icontains=query).annotate(
            store_amount=F('store__amount')).order_by(
            'subcategory__name',
            'name'
        )


class SubCategoryView(CategoryBase):
    """"Веб сервис для работы с номенклатурой
      (отображение, фильтрация) в зависимости от выбранной подкатегории."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = SubCategory.objects.get(pk=self.kwargs['pk']).name
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Nomenclature.objects.filter(
            Q(subcategory=self.kwargs['pk'])).filter(
            Q(name__icontains=query)
        ).annotate(store_amount=F('store__amount')).order_by('name')


class NomenclatureView(SuperUserRequiredMixin, DataMixin, DetailView):
    """"Веб сервис для работы с номенклатурой
      (отображение карточки)"""

    model = Nomenclature
    template_name = 'nomenclature/nomenclature.html'
    context_object_name = 'nomenclature'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context = dict(list(context.items()) + list(c_def.items()))

        subcategories = SubCategory.objects.filter(
            category=self.object.subcategory.category)

        context['subcategories'] = subcategories

        context['store'], _ = Store.objects.get_or_create(
            nomenclature=self.object)

        nomenclatures = Nomenclature.objects.filter(
            subcategory__in=subcategories)

        context['total_category'] = Store.objects.filter(
            nomenclature__in=nomenclatures).aggregate(
            sum=Sum(F('nomenclature__price') * F('amount'))).get('sum')

        return context


class NomenklatureAddView(SuperUserRequiredMixin, DataMixin, CreateView):
    """"Веб сервис для добавления номенклатуры. """

    form_class = NomenklatureAddForm
    template_name = 'nomenclature/nomenclature_add.html'
    success_url = reverse_lazy('nomenclature_list')
    #    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление номенклатуры')
        return dict(list(context.items()) + list(c_def.items()))

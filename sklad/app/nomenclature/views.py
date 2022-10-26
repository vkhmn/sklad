from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy


from app.core.mixin import SuperUserRequiredMixin, DataMixin
from app.core.forms import SearchForm
from .forms import NomenklatureAddForm
from .models import Nomenclature
from .services import get_subcats, get_nomenclatures_list, get_category_name

from .services import get_nomenclatures_category, get_subcategory_name
from .services import get_nomenclatures_subcategory, NomenclatureContext


class NomenclatureListView(SuperUserRequiredMixin, DataMixin, ListView):
    """Представление для отображения списка номеклатуры."""

    model = Nomenclature
    template_name = 'nomenclature/list.html'
    context_object_name = 'nomenclatures'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Номенклатура',
                subcats=get_subcats(),
                search_form=SearchForm(data=self.request.GET)
            )
        )
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return get_nomenclatures_list(query)


class CategoryBase(SuperUserRequiredMixin, DataMixin, ListView):
    """
    Базовый класс представления
    для отображения номеклатуры в зависимости от категории.
    """

    model = Nomenclature
    template_name = 'nomenclature/list.html'
    context_object_name = 'nomenclatures'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                subcats=get_subcats(),
                search_form=SearchForm(data=self.request.GET)
            )
        )
        return context


class CategoryView(CategoryBase):
    """Представление для отображения номеклатуры в зависимости от категории."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=get_category_name(self.kwargs.get('pk'))
        )
        return context

    def get_queryset(self):
        return get_nomenclatures_category(
            pk=self.kwargs.get('pk'),
            query=self.request.GET.get('search', '')
        )


class SubCategoryView(CategoryBase):
    """Представление для отображения номеклатуры в зависимости от подкатегории."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=get_subcategory_name(self.kwargs.get('pk'))
        )
        return context

    def get_queryset(self):
        return get_nomenclatures_subcategory(
            pk=self.kwargs.get('pk'),
            query=self.request.GET.get('search', '')
        )


class NomenclatureView(SuperUserRequiredMixin, DataMixin, DetailView):
    """Представление для отображения деталей номенклатуры."""

    model = Nomenclature
    template_name = 'nomenclature/details.html'
    context_object_name = 'nomenclature'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                **NomenclatureContext.execute(self.object)
            )
        )
        return context


class NomenklatureAddView(SuperUserRequiredMixin, DataMixin, CreateView):
    """Представление для создания новой номенклатуры."""

    form_class = NomenklatureAddForm
    template_name = 'nomenclature/add.html'
    success_url = reverse_lazy('nomenclature_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Добавление номенклатуры'
            )
        )
        return context
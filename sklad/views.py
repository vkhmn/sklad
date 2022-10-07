from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.db.models import Count

# from sklad.models import *
from sklad.mixin import DataMixin, SuperUserRequiredMixin
from sklad.forms import *
from sklad.tasks import send_email_to_buyer
from sklad.utils import decode


class IndexView(LoginRequiredMixin, DataMixin, ListView):
    """"Веб сервис отображающий главную страницу, с последними заявками на
    отгрузку (поставку) товара."""

    model = Document
    template_name = 'sklad/index.html'
    context_object_name = 'documents'
    extra_context = {'title': 'Заявки на поставку/отгрузку'}
    ordering = ['-time_create']
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class DeliveryListView(SuperUserRequiredMixin, IndexView):
    """"Веб сервис для работы с заявками на поставку."""
    extra_context = {
        'left_menu': [
            {'url_name': 'delivery_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на поставку',
    }

    def get_queryset(self):
        return Document.objects.filter(vendor__isnull=False).order_by('-time_create')


class ShipmentListView(SuperUserRequiredMixin, IndexView):
    """"Веб сервис для работы с заявками."""
    extra_context = {
        'left_menu': [
            {'url_name': 'shipment_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на отгрузку',
    }

    def get_queryset(self):
        return Document.objects.filter(buyer__isnull=False).order_by('-time_create')


class DocumentView(LoginRequiredMixin, DataMixin, DetailView):
    """" Веб сервис для работы с заявкой
    на поставку/отгрузку (отображение карточки) """

    model = Document
    template_name = 'sklad/document.html'
    context_object_name = 'document'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация по заявке")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class NomenclatureListView(SuperUserRequiredMixin, DataMixin, ListView):
    """"Веб сервис для работы с номенклатурой
    (отображение, поиск, добавление)."""

    model = Nomenclature
    template_name = 'sklad/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        context['subcats'] = SubCategory.objects.annotate(total=Count(
            'nomenclature')
        ).filter(total__gt=0).order_by('category__name', 'name')
        return context

    def get_queryset(self):
        return Nomenclature.objects.all().order_by(
            'subcategory__category__name',
            'subcategory__name',
            'name'
        )


class BuyerListView(SuperUserRequiredMixin, DataMixin, ListView):
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


class VendorListView(SuperUserRequiredMixin, DataMixin, ListView):
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


class CategoryView(SuperUserRequiredMixin, DataMixin, ListView):
    """"Веб сервис для работы с номенклатурой
    (отображение, фильтрация) в зависимости от выбранной категории."""

    model = Nomenclature
    template_name = 'sklad/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context = dict(list(context.items()) + list(c_def.items()))
        context['subcats'] = SubCategory.objects.annotate(total=Count(
            'nomenclature')
        ).filter(total__gt=0).order_by('category__name', 'name')
        return context

    def get_queryset(self):
        return Nomenclature.objects.filter(
            subcategory__category=self.kwargs['pk']
        ).order_by('subcategory__name', 'name')


class SubCategoryView(CategoryView, ListView):
    """"Веб сервис для работы с номенклатурой
      (отображение, фильтрация) в зависимости от выбранной подкатегории."""

    def get_queryset(self):
        return Nomenclature.objects.filter(
            subcategory=self.kwargs['pk']
        ).order_by('name')


class NomenclatureView(SuperUserRequiredMixin, DataMixin, DetailView):
    """"Веб сервис для работы с номенклатурой
      (отображение карточки)"""

    model = Nomenclature
    template_name = 'sklad/nomenclature.html'
    context_object_name = 'nomenclature'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class BuyerView(SuperUserRequiredMixin, DataMixin, DetailView):
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
        context['documents'] = Document.objects.filter(
            buyer=self.object).order_by('-time_create')
        return context


class VendorView(SuperUserRequiredMixin, DataMixin, DetailView):
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
        context['documents'] = Document.objects.filter(
            vendor=self.object).order_by('-time_create')

        return context


class NomenklatureAddView(SuperUserRequiredMixin, DataMixin, CreateView):
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


class BuyerAddView(SuperUserRequiredMixin, DataMixin, CreateView):
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
        context['url_name'] = 'buyer_add'
        return dict(list(context.items()) + list(c_def.items()))


class VendorAddView(SuperUserRequiredMixin, DataMixin, CreateView):
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
        context['url_name'] = 'vendor_add'
        return dict(list(context.items()) + list(c_def.items()))


class ShipmentAddView(SuperUserRequiredMixin, DataMixin, CreateView):
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


class DeliveryAddView(SuperUserRequiredMixin, DataMixin, CreateView):
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


class LoginUser(DataMixin, LoginView):
    """ Веб сервис для авторизации. """

    form_class = LoginUserForm
    template_name = 'sklad/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ConfirmView(DataMixin, TemplateView):
    """ Веб сервис для подтвеждения заказа покупателем """

    template_name = 'sklad/document_confirm.html'
    context_object_name = 'document'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Подтвеждение получения товара")
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        code = request.POST.get('code')
        if not code:
            raise Http404
        document_id = decode(code)
        d = get_object_or_404(Document, pk=document_id)
        context['document_id'] = document_id
        if d.status != Status.COLLECTED:
            raise Http404
        d.status = Status.FINISHED
        d.save()
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if not code:
            raise Http404
        context = self.get_context_data(**kwargs)
        document_id = decode(code)
        get_object_or_404(Document, pk=document_id)
        context['document_id'] = document_id
        return self.render_to_response(context)


def logout_user(request):
    """ Выход пользователя из аккаунта """

    logout(request)
    return redirect('login')


class UpdateStatusDocumentView(DocumentView):
    """ Веб сервис для обновления статуса заказа отгрузки """

    def get_context_data(self, *, object_list=None, **kwargs):
        status = self.kwargs.get('status')
        document_id = self.kwargs.get('pk')

        if status not in Status:
            raise Http404("Status code is not founded")

        self.object.status = status
        self.object.save()

        if status in (Status.CANCELED, Status.COLLECTED):
            send_email_to_buyer.delay(document_id, status)

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация по заявке")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

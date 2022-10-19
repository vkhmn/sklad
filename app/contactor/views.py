from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import BuyerAddForm, BankDetailsAddForm, VendorAddForm
from .models import Buyer, Vendor
from app.core.mixin import SuperUserRequiredMixin, DataMixin
from app.document.models import Document


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
        return dict(list(context.items()) + list(c_def.items()))


class VendorAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """"Веб сервис для добавления поставщика. """

    template_name = 'sklad/vendor_add.html'
    success_url = reverse_lazy('vendor_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление поставщика')
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        context['bank_details_form'] = BankDetailsAddForm()
        context['vendor_form'] = VendorAddForm()
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        bank_details_form = BankDetailsAddForm(request.POST)
        vendor_form = VendorAddForm(request.POST)
        if bank_details_form.is_valid() or vendor_form.is_valid():
            bd_form = bank_details_form.save(commit=False)
            bank_details_form.save()
            v_form = vendor_form.save(commit=False)
            v_form.bank_details = bd_form
            vendor_form.save()
        return redirect(self.success_url)

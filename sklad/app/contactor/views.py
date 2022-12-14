from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from app.core.mixin import SuperUserRequiredMixin
from app.contactor.forms import PersonAddForm, BankDetailsAddForm, VendorAddForm
from app.contactor.models import Buyer, Vendor
from app.contactor.services import (
    create_object, get_documents, create_vendor, get_buyers, get_vendors
)


class BuyerAddView(SuperUserRequiredMixin, CreateView):
    """Представление для добавления нового покупателя."""

    model = Buyer
    form_class = PersonAddForm
    template_name = 'contactor/buyer_add.html'
    success_url = reverse_lazy('buyer_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Создание покупателя'
        )
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        create_object(self.model, person=self.object)
        return FormMixin.form_valid(self, form)


class BuyerListView(SuperUserRequiredMixin, ListView):
    """Представление для отображения списка покупателей."""

    model = Buyer
    template_name = 'contactor/buyer_list.html'
    context_object_name = 'buyers'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Покупатели',
            create_url='buyer_add'
        )
        return context

    def get_queryset(self):
        return get_buyers()


class BuyerView(SuperUserRequiredMixin, DetailView):
    """Представление для отображения детальной информации о покупателе."""

    model = Buyer
    template_name = 'contactor/buyer_details.html'
    context_object_name = 'buyer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Сведения о покупателе',
            documents=get_documents(buyer=self.object, count=10)
        )
        return context


class VendorAddView(SuperUserRequiredMixin, TemplateView):
    """Отображение для добавления нового поставщика."""

    template_name = 'contactor/vendor_add.html'
    success_url = reverse_lazy('vendor_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Создание поставщика',
            bank_details_form=BankDetailsAddForm(),
            vendor_form=VendorAddForm(),
            contact_person_form=PersonAddForm()
        )
        return context

    def form_invalid(self, form):
        """Если форма не валидна, возвращаем страницу с данными формы."""
        contex = self.get_context_data()
        contex.update(form)
        return self.render_to_response(contex)

    def post(self, request, *args, **kwargs):
        forms = {
            'vendor_form': VendorAddForm(request.POST),
            'contact_person_form': PersonAddForm(request.POST),
            'bank_details_form': BankDetailsAddForm(request.POST),
        }
        # Валидация формы. Если форма не валидна то возвращаем страницу с данными формы.
        for form in forms.values():
            if not form.is_valid():
                return self.form_invalid(forms)

        # Сохрание данных формы в БД.
        create_vendor(forms)
        return redirect(self.success_url)


class VendorListView(SuperUserRequiredMixin, ListView):
    """Отображение для списка поставщиков."""

    model = Vendor
    template_name = 'contactor/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Поставщики',
            create_url='vendor_add',
        )
        return context

    def get_queryset(self):
        return get_vendors()


class VendorView(SuperUserRequiredMixin, DetailView):
    """Отображение для деталей поставщика и его последних документов."""

    model = Vendor
    template_name = 'contactor/vendor_details.html'
    context_object_name = 'vendor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Сведения о поставщике',
            documents=get_documents(vendor=self.object, count=10)
        )
        return context

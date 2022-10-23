from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from .enums import buyer_menu, vendor_menu
from .forms import PersonAddForm, BankDetailsAddForm, VendorAddForm
from .models import Buyer, Vendor
from app.core.mixin import SuperUserRequiredMixin, DataMixin
from .services import create_object, get_documents, create_vendor, get_buyers, get_vendors


class BuyerAddView(SuperUserRequiredMixin, DataMixin, CreateView):
    """Add new buyer."""

    model = Buyer
    form_class = PersonAddForm
    template_name = 'contactor/buyer_add.html'
    success_url = reverse_lazy('buyer_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Добавление покупателя'
            )
        )
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        create_object(self.model, person=self.object)
        return FormMixin.form_valid(self, form)


class BuyerListView(SuperUserRequiredMixin, DataMixin, ListView):
    """Render Buyer list."""

    model = Buyer
    template_name = 'contactor/buyer_list.html'
    context_object_name = 'buyers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Покупатели',
                left_menu=buyer_menu
            )
        )
        return context

    def get_queryset(self):
        return get_buyers()


class BuyerView(SuperUserRequiredMixin, DataMixin, DetailView):
    """ Render Buyer details and his documents. """

    model = Buyer
    template_name = 'contactor/buyer_details.html'
    context_object_name = 'buyer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Сведения о покупателе',
                left_menu=buyer_menu,
                documents=get_documents(buyer=self.object)
            )
        )
        return context


class VendorAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """Add new vendor."""

    template_name = 'contactor/vendor_add.html'
    success_url = reverse_lazy('vendor_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Добавление поставщика',
                bank_details_form=BankDetailsAddForm(),
                vendor_form=VendorAddForm(),
                contact_person_form=PersonAddForm()
            )
        )
        return context

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        contex = self.get_context_data()
        contex.update(form)
        return self.render_to_response(contex)

    def post(self, request, *args, **kwargs):
        forms = {
            'vendor_form': VendorAddForm(request.POST),
            'contact_person_form': PersonAddForm(request.POST),
            'bank_details_form': BankDetailsAddForm(request.POST),
        }
        # Validate forms
        for form in forms.values():
            if not form.is_valid():
                return self.form_invalid(forms)

        # Save forms
        create_vendor(forms)
        return redirect(self.success_url)


class VendorListView(SuperUserRequiredMixin, DataMixin, ListView):
    """Render Vendor list."""

    model = Vendor
    template_name = 'contactor/vendor_list.html'
    context_object_name = 'vendors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Поставщики',
                left_menu=vendor_menu
            )
        )
        return context

    def get_queryset(self):
        return get_vendors()


class VendorView(SuperUserRequiredMixin, DataMixin, DetailView):
    """ Render Vendor details and his documents. """

    model = Vendor
    template_name = 'contactor/vendor_details.html'
    context_object_name = 'vendor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Сведения о поставщике',
                left_menu=buyer_menu,
                documents=get_documents(vendor=self.object)
            )
        )
        return context

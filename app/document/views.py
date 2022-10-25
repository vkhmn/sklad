from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse


from app.core.mixin import DataMixin, SuperUserRequiredMixin
from app.core.forms import SearchForm
from .enums import delivery_menu, shipment_menu
from .forms import DeliveryAddForm, DocumentNomenclaturesFormSet
from .forms import ShipmentAddForm
from .models import Document, Status
from .services import (
    get_documents_filter,
    get_deliveries_filter,
    get_shipments_filter,
    DocumentContext,
    DocumentAdd,
    ConfirmDocument,
    ChangeDocumentStatus
)


class HomeView(LoginRequiredMixin, DataMixin, ListView):
    """Представление для главной страницы."""

    model = Document
    template_name = 'core/index.html'
    context_object_name = 'documents'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Заявки на поставку/отгрузку',
                search_form=SearchForm(data=self.request.GET)
            )
        )
        return context

    def get_params(self):
        query = self.request.GET.get('search', '')
        status = self.request.GET.get('status')
        status = (status, ) if status else Status
        return query, status

    def get_queryset(self):
        return get_documents_filter(*self.get_params())


class DeliveryListView(SuperUserRequiredMixin, HomeView):
    """Представление для отображения списка документов на поставку."""

    extra_context = {
        'left_menu': delivery_menu,
        'title': 'Заявки на поставку',
    }

    def get_queryset(self):
        return get_deliveries_filter(*self.get_params())


class ShipmentListView(SuperUserRequiredMixin, HomeView):
    """Представление для отображения списка документов на отгрузку."""

    extra_context = {
        'left_menu': shipment_menu,
        'title': 'Заявки на отгрузку',
    }

    def get_queryset(self):
        return get_shipments_filter(*self.get_params())


class DocumentView(LoginRequiredMixin, DataMixin, DetailView):
    """Представление для отображения деталей документа."""

    model = Document
    template_name = 'document/details.html'
    context_object_name = 'document'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Информация по заявке',
                **DocumentContext.execute(self.object)
            )
        )
        return context


class DocumentAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """Базовый класс представления для создания документа."""

    template_name = 'document/add.html'
    success_url = None
    contactor = None

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        contex = self.get_context_data()
        contex.update(form)
        return self.render_to_response(contex)

    def post(self, request, *args, **kwargs):
        forms = {
            'document_add_form': None,
            'document_nomenclature_form_set': DocumentNomenclaturesFormSet(
                data=request.POST
            ),
        }
        forms.update(kwargs)
        # Validate forms
        for form in forms.values():
            if not form.is_valid():
                return self.form_invalid(forms)

        if not DocumentAdd.execute(forms, self.contactor):
            _, nomenclatures_form_set = forms.values()
            form, *_ = nomenclatures_form_set.forms
            form.add_error(None, 'Укажите корректные данные для номенклатуры')
            return self.form_invalid(forms)

        return redirect(self.success_url)


class DeliveryAddView(DocumentAddView):
    """Представление для создания документа на поставку."""

    success_url = reverse_lazy('delivery_list')
    contactor = 'vendor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Создание заяки на поставку',
                document_add_form=DeliveryAddForm(),
                document_nomenclature_form_set=DocumentNomenclaturesFormSet()
            )
        )
        return context

    def post(self, request, *args, **kwargs):
        kwargs.update(
            document_add_form=DeliveryAddForm(request.POST)
        )
        return super().post(request, *args, **kwargs)


class ShipmentAddView(DocumentAddView):
    """Отображание для создания документа на отгрузку."""

    success_url = reverse_lazy('shipment_list')
    contactor = 'buyer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Создание заяки отгрузку',
                document_add_form=ShipmentAddForm(),
                document_nomenclature_form_set=DocumentNomenclaturesFormSet()
            )
        )
        return context

    def post(self, request, *args, **kwargs):
        kwargs.update(
            document_add_form=ShipmentAddForm(request.POST)
        )
        return super().post(request, *args, **kwargs)


class ConfirmView(DataMixin, TemplateView):
    """Отображение для подтвеждения получения товара покупателем."""

    template_name = 'document/confirm.html'
    context_object_name = 'document'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(title="Подтвеждение получения товара")
        )
        return context

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        context = self.get_context_data(**kwargs)
        context.update(
            ConfirmDocument.execute(code, change_status=True)
        )
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        context = self.get_context_data(**kwargs)
        context.update(
            ConfirmDocument.execute(code, change_status=False)
        )
        return self.render_to_response(context)


class UpdateStatusDocumentView(DocumentView):
    """Представление для изменения статуса документа."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(title="Информация по заявке")
        )
        return context

    def get(self, request, *args, **kwargs):
        # Получить объект документа - self.object
        super().get(self, request, *args, **kwargs)
        status = self.kwargs.get('status')
        ChangeDocumentStatus.execute(self.object, status)
        return redirect(
            reverse(
                'document',
                args={self.object.pk: self.object.pk}
            )
        )

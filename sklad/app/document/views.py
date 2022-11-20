from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse


from app.core.mixin import SuperUserRequiredMixin
from app.core.forms import SearchForm
from app.document.forms import (
    DeliveryAddForm, DocumentNomenclaturesFormSet, ShipmentAddForm
)
from app.document.models import Document, Status
from app.document.services import (
    get_documents_filter, get_deliveries_filter, get_shipments_filter,
    DocumentContext, DocumentAdd, ConfirmDocument, ChangeDocumentStatus,
    get_documents_status
)


class HomeView(LoginRequiredMixin, ListView):
    """Представление для главной страницы."""

    model = Document
    template_name = 'core/index.html'
    context_object_name = 'documents'
    login_url = reverse_lazy('login')
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Заявки на поставку/отгрузку',
            search_form=SearchForm(data=self.request.GET),
            st=get_documents_status(*self.get_params())
        )
        return context

    def get_params(self):
        query = self.request.GET.get('search', '')
        status = self.request.GET.get('status')
        status = status.split(',') if status else Status
        return query, status

    def get_queryset(self):
        return get_documents_filter(*self.get_params())


class DeliveryListView(SuperUserRequiredMixin, HomeView):
    """Представление для отображения списка документов на поставку."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Заявки на поставку',
            create_url='delivery_add',
            st=get_documents_status(*self.get_params(), document='delivery')
        )
        return context

    def get_queryset(self):
        return get_deliveries_filter(*self.get_params())


class ShipmentListView(SuperUserRequiredMixin, HomeView):
    """Представление для отображения списка документов на отгрузку."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Заявки на отгрузку',
            create_url='shipment_add',
            st=get_documents_status(*self.get_params(), document='shipment')
        )
        return context

    def get_queryset(self):
        return get_shipments_filter(*self.get_params())


class DocumentView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей документа."""

    model = Document
    template_name = 'document/details.html'
    context_object_name = 'document'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Информация по заявке',
            **DocumentContext.execute(self.object)
        )
        return context


class DocumentAddView(SuperUserRequiredMixin, TemplateView):
    """Базовый класс представления для создания документа."""

    template_name = 'document/add.html'
    success_url = None
    contactor = None

    def form_invalid(self, form):
        """Если форма не валидна, то вывести контекст для формы."""
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
        # Проверка формы на валидность
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
            title='Создание заяки на поставку',
            document_add_form=DeliveryAddForm(),
            document_nomenclature_form_set=DocumentNomenclaturesFormSet()
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
            title='Создание заяки на отгрузку',
            document_add_form=ShipmentAddForm(),
            document_nomenclature_form_set=DocumentNomenclaturesFormSet()
        )
        return context

    def post(self, request, *args, **kwargs):
        kwargs.update(
            document_add_form=ShipmentAddForm(request.POST)
        )
        return super().post(request, *args, **kwargs)


class ConfirmView(TemplateView):
    """Отображение для подтвеждения получения товара покупателем."""

    template_name = 'document/confirm.html'
    context_object_name = 'document'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title="Подтвеждение получения товара"
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


class ChangeDocumentStatusView(DocumentView):
    """Представление для изменения статуса документа."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title="Информация по заявке"
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

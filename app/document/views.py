from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, F, Min, Q


from app.core.mixin import DataMixin, SuperUserRequiredMixin
from app.core.forms import SearchForm
from app.core.utils import make_qrcode, decode
from app.nomenclature.models import Store
from .enams import delivery_menu, shipment_menu
from .forms import DeliveryAddForm, DocumentNomenclaturesFormSet
from .forms import ShipmentAddForm
from .models import Document, Status, DocumentNomenclatures
from .services import get_documents_filter, get_deliveries_filter, \
    get_shipments_filter, get_total, get_nomenclatures, create_document
from .tasks import send_email_to_buyer


class HomeView(LoginRequiredMixin, DataMixin, ListView):
    """Render home page with all documents."""

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
    """Render page with all delivery documents."""

    extra_context = {
        'left_menu': delivery_menu,
        'title': 'Заявки на поставку',
    }

    def get_queryset(self):
        return get_deliveries_filter(*self.get_params())


class ShipmentListView(SuperUserRequiredMixin, HomeView):
    """Render page with all delivery documents."""

    extra_context = {
        'left_menu': shipment_menu,
        'title': 'Заявки на отгрузку',
    }

    def get_queryset(self):
        return get_shipments_filter(*self.get_params())


class DocumentView(LoginRequiredMixin, DataMixin, DetailView):
    """Render document details."""

    model = Document
    template_name = 'document/details.html'
    context_object_name = 'document'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_context(
                title='Информация по заявке',
                qrcode=make_qrcode(self.object.pk),
                total=get_total(self.object),
                result=get_nomenclatures(self.object)
            )
        )
        return context


class DocumentAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """Base class for adding document."""

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

        if not create_document(forms, self.contactor):
            _, nomenclatures_form_set = forms.values()
            form, *_ = nomenclatures_form_set.forms
            form.add_error(None, 'Укажите корректные данные для номенклатуры')
            return self.form_invalid(forms)

        return redirect(self.success_url)


class DeliveryAddView(DocumentAddView):
    """Add new delivery document."""

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
            {
                'document_add_form': DeliveryAddForm(request.POST)
            }
        )
        return super().post(request, *args, **kwargs)


class ShipmentAddView(DocumentAddView):
    """Add new shipment document."""

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
            {
                'document_add_form': ShipmentAddForm(request.POST)
            }
        )
        return super().post(request, *args, **kwargs)


class ConfirmView(DataMixin, TemplateView):
    """ Веб сервис для подтвеждения заказа покупателем """

    template_name = 'document/confirm.html'
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


class UpdateStatusDocumentView(DocumentView):
    """ Веб сервис для обновления статуса заказа отгрузки """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация по заявке")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        status = self.kwargs.get('status')
        document_id = self.kwargs.get('pk')

        if status not in Status:
            raise Http404("Status code is not founded")

        if self.object.status in (Status.FINISHED, status):
            raise Http404("Can't change Status code")

        self.object.status = status
        self.object.save()

        if self.object.vendor is not None:
            if status in (Status.FINISHED, ):
                # Add nomenclatures amount to Store
                for item in DocumentNomenclatures.objects.filter(document=self.object):
                    Store.objects.filter(nomenclature=item.nomenclature).update(
                        amount=F('amount') + item.amount
                    )

        if self.object.buyer is not None:
            if status in (Status.CANCELED, Status.COLLECTED):
                send_email_to_buyer.delay(document_id, status)

            if status in (Status.COLLECTED, ):
                # Sub nomenclatures amount to Store (Reserve)
                for item in DocumentNomenclatures.objects.filter(document=self.object):
                    Store.objects.filter(nomenclature=item.nomenclature).update(
                        amount=F('amount') - item.amount
                    )
        return redirect(reverse('document', args={document_id: document_id}))

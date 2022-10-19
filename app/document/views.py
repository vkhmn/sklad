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
from .forms import DeliveryAddForm, DocumentNomenclaturesFormSet
from .forms import ShipmentAddForm
from .models import Document, Status, Store, DocumentNomenclatures
from .tasks import send_email_to_buyer


class IndexView(LoginRequiredMixin, DataMixin, ListView):
    """"Веб сервис отображающий главную страницу, с последними заявками на
    отгрузку (поставку) товара."""

    model = Document
    template_name = 'sklad/index.html'
    context_object_name = 'documents'
    extra_context = {'title': 'Заявки на поставку/отгрузку'}
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        context['search_form'] = SearchForm(data=self.request.GET)
        return context

    def get_query_search(self):
        return self.request.GET.get('search', '')

    def get_status(self):
        status = self.request.GET.get('status')
        status = (status, ) if status else Status
        return status

    def get_queryset(self):
        query = self.get_query_search()
        status = self.get_status()
        return Document.objects.filter(
            Q(vendor__name__icontains=query) | Q(buyer__fio__icontains=query)
        ).filter(status__in=status).order_by('-time_create')


class DeliveryListView(SuperUserRequiredMixin, IndexView):
    """"Веб сервис для работы с заявками на поставку."""
    extra_context = {
        'left_menu': [
            {'url_name': 'delivery_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на поставку',
    }

    def get_queryset(self):
        query = self.get_query_search()
        status = self.get_status()
        return Document.objects.filter(
            vendor__isnull=False).filter(
            vendor__name__icontains=query).filter(
            status__in=status).order_by('-time_create')


class ShipmentListView(SuperUserRequiredMixin, IndexView):
    """"Веб сервис для работы с заявками."""
    extra_context = {
        'left_menu': [
            {'url_name': 'shipment_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на отгрузку',
    }

    def get_queryset(self):
        query = self.get_query_search()
        status = self.get_status()
        return Document.objects.filter(
            buyer__isnull=False).filter(
            buyer__fio__icontains=query).filter(
            status__in=status).order_by('-time_create')


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
        context['qrcode'] = make_qrcode(self.object.pk)

        # Select Sum(price * amount), Min(store.amount - amount)
        # for document.nomenclatures
        context['total'] = self.object.nomenclatures.aggregate(
            sum=Sum(F('documentnomenclatures__amount') * F('price')),
            min=Min(F('store__amount') - F('documentnomenclatures__amount'))
        )

        # Select price * amount, amount, store.amount
        # for each document.nomenclatures
        context['result'] = self.object.nomenclatures.annotate(
            total=F('documentnomenclatures__amount') * F('price'),
            amount=F('documentnomenclatures__amount'),
            store_amount=F('store__amount')
        )
        return context


class DeliveryAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """"Веб сервис для создания заявки на поставку. """

    template_name = 'sklad/document_add.html'
    success_url = reverse_lazy('delivery_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание заяки на поставку')
        context['document_add_form'] = DeliveryAddForm()
        context['document_nomenclature_form_set'] = DocumentNomenclaturesFormSet()
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        document_add_form = DeliveryAddForm(request.POST)
        document_nomenclature_form_set = DocumentNomenclaturesFormSet(
            data=request.POST
        )
        if document_add_form.is_valid() or document_nomenclature_form_set.is_valid():
            print(document_add_form.is_valid())
            document = Document(
                vendor=document_add_form.cleaned_data.get('contactor')
            )

            # Generate valid nomenclatures list
            nomenclatures = []
            for form in document_nomenclature_form_set:
                print(form.is_valid())
                try:
                    nomenclature = DocumentNomenclatures(
                        **form.cleaned_data,
                        document=document
                    )
                    nomenclature.full_clean(exclude=['document'])
                    nomenclatures.append(nomenclature)
                except ValidationError:
                    print('Error')

            if nomenclatures:
                document.save()

                # Merge dublicate nomenclature item
                nomenclatures_dict = dict()
                for n in nomenclatures:
                    if n.nomenclature in nomenclatures_dict:
                        nomenclatures_dict[n.nomenclature].amount += n.amount
                    else:
                        nomenclatures_dict[n.nomenclature] = n

                [nomenclature.save() for nomenclature in nomenclatures_dict.values()]
            else:
                document_add_form.add_error(
                    None,
                    'Укажите корректные данные для номенклатуры'
                )
                context = self.get_context_data(*args, **kwargs)
                context['document_add_form'] = document_add_form
                context['document_nomenclature_form_set'] = document_nomenclature_form_set
                return self.render_to_response(context)

        return redirect(self.success_url)


class ShipmentAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """"Веб сервис для создания заявки на отгрузку. """

    template_name = 'sklad/document_add.html'
    success_url = reverse_lazy('shipment_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание заявки на отгрузку')
        context['document_add_form'] = ShipmentAddForm()
        context['document_nomenclature_form_set'] = DocumentNomenclaturesFormSet()
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        document_add_form = ShipmentAddForm(request.POST)
        document_nomenclature_form_set = DocumentNomenclaturesFormSet(
            data=request.POST
        )
        if document_add_form.is_valid() or document_nomenclature_form_set.is_valid():
            print(document_add_form.is_valid())
            document = Document(
                buyer=document_add_form.cleaned_data.get('contactor')
            )

            # Generate valid nomenclatures list
            nomenclatures = []
            for form in document_nomenclature_form_set:
                print(form.is_valid())
                try:
                    nomenclature = DocumentNomenclatures(
                        **form.cleaned_data,
                        document=document
                    )
                    nomenclature.full_clean(exclude=['document'])
                    nomenclatures.append(nomenclature)
                except ValidationError:
                    print('Error')

            if nomenclatures:
                document.save()

                # Merge dublicate nomenclature item
                nomenclatures_dict = dict()
                for n in nomenclatures:
                    if n.nomenclature in nomenclatures_dict:
                        nomenclatures_dict[n.nomenclature].amount += n.amount
                    else:
                        nomenclatures_dict[n.nomenclature] = n

                [nomenclature.save() for nomenclature in nomenclatures_dict.values()]
            else:
                document_add_form.add_error(
                    None,
                    'Укажите корректные данные для номенклатуры'
                )
                context = self.get_context_data(*args, **kwargs)
                context['document_add_form'] = document_add_form
                context['document_nomenclature_form_set'] = document_nomenclature_form_set
                return self.render_to_response(context)

        return redirect(self.success_url)


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

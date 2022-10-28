from operator import xor
from typing import Callable

from django.core.exceptions import ValidationError
from django.db.models import Sum, F, Min, Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from app.document.models import Document, DocumentNomenclatures, Status
from app.document.enums import messages
from app.document.tasks.task1 import send_email_to_buyer
from app.nomenclature.models import Store
from app.core.utils import decode, make_qrcode, get_confirm_url


def get_documents_filter(query, status):
    return Document.objects.select_related('vendor', 'buyer__person').filter(
        (
           Q(vendor__name__icontains=query) |
           Q(buyer__person__full_name__icontains=query)
        ) & Q(status__in=status)
    ).order_by('-time_create')


def get_deliveries_filter(query, status):
    return Document.objects.select_related('vendor').filter(
        Q(vendor__isnull=False) &
        Q(vendor__name__icontains=query) &
        Q(status__in=status)
    ).order_by('-time_create')


def get_shipments_filter(query, status):
    return Document.objects.select_related('buyer__person').filter(
        Q(buyer__isnull=False) &
        Q(buyer__person__full_name__icontains=query) &
        Q(status__in=status)
    ).order_by('-time_create')


class DocumentContext:
    """Возвращает контекст для документа."""

    @classmethod
    def _get_total(cls, document):
        # Select Sum(price * amount), Min(store.amount - amount)
        # for document.nomenclatures
        return document.nomenclatures.aggregate(
            sum=Sum(F('documentnomenclatures__amount') * F('price')),
            min=Min(F('store__amount') - F('documentnomenclatures__amount'))
        )

    @classmethod
    def _get_nomenclatures(cls, document):
        # Select price * amount, amount, store.amount
        # for each document.nomenclatures
        return document.nomenclatures.annotate(
            total=F('documentnomenclatures__amount') * F('price'),
            amount=F('documentnomenclatures__amount'),
            store_amount=F('store__amount')
        )

    @classmethod
    def execute(cls, document):
        return dict(
            qrcode=make_qrcode(document.pk),
            total=cls._get_total(document),
            result=cls._get_nomenclatures(document)
        )


class DocumentAdd:
    """Создание документа."""

    @classmethod
    def _validate_nomenclatures(cls, form_set):
        nomenclatures = []
        for form in form_set:
            try:
                nomenclature = DocumentNomenclatures(
                    **form.cleaned_data,
                )
                nomenclature.full_clean(exclude=['document'])
                nomenclatures.append(nomenclature)
            except ValidationError:
                pass

        return nomenclatures

    @classmethod
    def _merge_dublicate_nomenclature(cls, nomenclatures):
        """Объединить одинаковые позиции документа."""

        nomenclatures_dict = dict()
        for n in nomenclatures:
            if n.nomenclature in nomenclatures_dict:
                nomenclatures_dict[n.nomenclature].amount += n.amount
            else:
                nomenclatures_dict[n.nomenclature] = n
        return nomenclatures_dict.values()

    @classmethod
    def _create_document(cls, forms, contactor):
        document_form, nomenclatures_form_set = forms.values()
        nomenclatures = cls._validate_nomenclatures(nomenclatures_form_set)

        if not nomenclatures:
            return False

        nomenclatures = cls._merge_dublicate_nomenclature(nomenclatures)
        document = Document.objects.create(**{
            contactor: document_form.cleaned_data.get('contactor')
        })
        for nomenclature in nomenclatures:
            nomenclature.document = document
        DocumentNomenclatures.objects.bulk_create(
            nomenclatures
        )
        return True

    @classmethod
    def execute(cls, forms, contactor):
        return cls._create_document(forms, contactor)


class ConfirmDocument:
    """Подверждение получения товара покупателем. (COLLECTED -> FINISHED)."""

    @classmethod
    def _get_document_or_404(cls, code):
        if not code:
            raise Http404
        document_id = decode(code)
        return get_object_or_404(Document, pk=document_id)

    @classmethod
    def execute(cls, code, change_status=False):
        document = cls._get_document_or_404(code)
        if change_status:
            ChangeDocumentStatus.execute(document, Status.FINISHED)
        return dict(document_id=document.pk)


class ChangeDocumentStatus:
    """Изменение статуса документа."""

    @classmethod  #
    def _change_status(cls, document: Document, status: str) -> None:
        document.status = status
        document.save()

    @classmethod
    def _send_message(cls, document, status):
        message = messages.get((document.status, status))
        email = document.buyer.person.email
        if message and email:
            confirm_url = get_confirm_url(document.pk)
            if status == Status.COLLECTED:
                message.update(
                    confirm_url=confirm_url,
                    qrcode=make_qrcode(document.pk)
                )
            send_email_to_buyer.delay(email, message)
        else:
            print(message, email, (document.status, status))
            print('Письмо не отправлено')

    @classmethod  #
    def _buyer_va_co(cls, document: Document, status: str) -> None:
        cls._decrease_store_amount(document)
        cls._send_message(document, status)
        cls._change_status(document, status)

    @classmethod  #
    def _buyer_va_ca(cls, document: Document, status: str) -> None:
        cls._send_message(document, status)
        cls._change_status(document, status)

    @classmethod  #
    def _buyer_co_ca(cls, document: Document, status: str) -> None:
        cls._increase_store_amount(document)
        cls._send_message(document, status)
        cls._change_status(document, status)

    @classmethod  #
    def _vendor_va_fi(cls, document: Document, status: str) -> None:
        cls._increase_store_amount(document)
        cls._change_status(document, status)

    @classmethod
    def _increase_store_amount(cls, document: Document) -> None:
        for item in DocumentNomenclatures.objects.filter(document=document):
            Store.objects.filter(nomenclature=item.nomenclature).update(
                amount=F('amount') + item.amount
            )

    @classmethod
    def _decrease_store_amount(cls, document: Document) -> None:
        for item in DocumentNomenclatures.objects.filter(document=document):
            Store.objects.filter(nomenclature=item.nomenclature).update(
                amount=F('amount') - item.amount
            )

    @classmethod
    def _get_transitions(cls, begin_state: str, end_state: str) -> tuple:
        return begin_state, end_state

    @classmethod
    def _document_incorrect(cls):
        raise Http404("Документ не корректный!")

    @classmethod
    def _transions_not_found(cls, *args):
        raise Http404("Невозможно изменить текущий статус!")

    @classmethod
    def execute(cls, document: Document, status: str) -> None:
        vendor_transitions = {
            (Status.VALIDATING, Status.CANCELED): cls._change_status,
            (Status.VALIDATING, Status.FINISHED): cls._vendor_va_fi,
        }
        buyer_transitions = {
            (Status.VALIDATING, Status.COLLECTED): cls._buyer_va_co,
            (Status.VALIDATING, Status.CANCELED): cls._buyer_va_ca,
            (Status.COLLECTED, Status.CANCELED): cls._buyer_co_ca,
            (Status.COLLECTED, Status.FINISHED): cls._change_status,
        }

        if not xor(bool(document.vendor), bool(document.buyer)):
            cls._document_incorrect()  # raise Http404

        if document.vendor:
            contactor = vendor_transitions
        else:
            contactor = buyer_transitions

        func: Callable[[Document, str], None] = contactor.get(
            cls._get_transitions(document.status, status),
            cls._transions_not_found
        )
        func(document, status)

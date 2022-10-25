from django.core.exceptions import ValidationError
from django.db.models import Sum, F, Min, Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Document, DocumentNomenclatures, Status
from .tasks import send_email_to_buyer
from app.nomenclature.models import Store
from app.core.utils import decode, make_qrcode


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
    def _change_document_status_confirm(cls, document):
        if document.status != Status.COLLECTED:
            raise Http404
        document.status = Status.FINISHED
        document.save()

    @classmethod
    def execute(cls, code, change_status=False):
        document = cls._get_document_or_404(code)
        if change_status:
            cls._change_document_status_confirm(document)
        return dict(document_id=document.pk)


class ChangeDocumentStatus:
    """Изменение статуса документа."""

    @classmethod
    def _change_status(cls, document, status):
        # Проверка на корректность передаваемого статуса.
        if status not in Status:
            raise Http404("Код статуса не найден!")

        # Текущий статус документа равен статусу Завершен,
        # либо равен пердаваемому статусу.
        if document.status in (Status.FINISHED, status):
            raise Http404("Невозможно изменить текущий статус документа!")

        document.status = status
        document.save()

    @classmethod
    def _increase_store_amount(cls, document):
        for item in DocumentNomenclatures.objects.filter(document=document):
            Store.objects.filter(nomenclature=item.nomenclature).update(
                amount=F('amount') + item.amount
            )

    @classmethod
    def _decrease_store_amount(cls, document):
        for item in DocumentNomenclatures.objects.filter(document=document):
            Store.objects.filter(nomenclature=item.nomenclature).update(
                amount=F('amount') - item.amount
            )

    @classmethod
    def execute(cls, document, status):
        cls._change_status(document, status)
        # Увеличить количество номенлатуры на складе (Поставка).
        if document.vendor is not None:
            if status in (Status.FINISHED,):
                cls._increase_store_amount(document)
        # Уменьшить количество номенклатуры на складе (Отгрузка)
        elif document.buyer is not None:
            if status in (Status.CANCELED, Status.COLLECTED):
                send_email_to_buyer.delay(document.pk, status)
            if status in (Status.COLLECTED,):
                cls._decrease_store_amount(document)

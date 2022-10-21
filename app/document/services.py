from django.core.exceptions import ValidationError
from django.db.models import Sum, F, Min, Q
from .models import Document, DocumentNomenclatures


def get_documents_filter(query, status):
    return Document.objects.filter(
        Q(vendor__name__icontains=query) |
        Q(buyer__person__full_name__icontains=query)).filter(
        status__in=status).order_by('-time_create')


def get_deliveries_filter(query, status):
    return Document.objects.filter(
        vendor__isnull=False).filter(
        vendor__name__icontains=query).filter(
        status__in=status).order_by('-time_create')


def get_shipments_filter(query, status):
    return Document.objects.filter(
        buyer__isnull=False).filter(
        buyer__person__full_name__icontains=query).filter(
        status__in=status).order_by('-time_create')


def get_total(document):
    # Select Sum(price * amount), Min(store.amount - amount)
    # for document.nomenclatures
    return document.nomenclatures.aggregate(
        sum=Sum(F('documentnomenclatures__amount') * F('price')),
        min=Min(F('store__amount') - F('documentnomenclatures__amount'))
    )


def get_nomenclatures(document):
    # Select price * amount, amount, store.amount
    # for each document.nomenclatures
    return document.nomenclatures.annotate(
        total=F('documentnomenclatures__amount') * F('price'),
        amount=F('documentnomenclatures__amount'),
        store_amount=F('store__amount')
    )


def validate_nomenclatures(form_set):
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


def merge_dublicate_nomenclature(nomenclatures):
    """Merge dublicate nomenclature item."""

    nomenclatures_dict = dict()
    for n in nomenclatures:
        if n.nomenclature in nomenclatures_dict:
            nomenclatures_dict[n.nomenclature].amount += n.amount
        else:
            nomenclatures_dict[n.nomenclature] = n
    return nomenclatures_dict.values()


def create_document(forms, contactor):
    document_form, nomenclatures_form_set = forms.values()
    nomenclatures = validate_nomenclatures(nomenclatures_form_set)

    if not nomenclatures:
        return False

    nomenclatures = merge_dublicate_nomenclature(nomenclatures)
    document = Document.objects.create(**{
        contactor: document_form.cleaned_data.get('contactor')
    })
    for nomenclature in nomenclatures:
        nomenclature.document = document
        nomenclature.save()
    return True




from app.contactor.models import Buyer, Vendor
from app.document.models import Document


def get_documents(count=5, **fields):
    return Document.objects.select_related(
        'vendor', 'buyer__person').filter(
        **fields
    ).order_by('-time_create')[:count]


def get_buyers():
    return Buyer.objects.select_related('person')


def get_vendors():
    return Vendor.objects.select_related('contact_person')


def create_object(model, **fields):
    model.objects.create(**fields)


def create_vendor(forms):
    vendor, contact_person, bank_details = forms.keys()
    vendor_object = forms[vendor].save(commit=False)
    vendor_object.contact_person = forms[contact_person].save()
    vendor_object.bank_details = forms[bank_details].save()
    forms[vendor].save()

from app.document.models import Document


def get_documents(**fields):
    return Document.objects.filter(**fields).order_by('-time_create')


def create_object(model, **fields):
    model.objects.create(**fields)


def create_vendor(forms):
    vendor, contact_person, bank_details = forms.keys()
    vendor_object = forms[vendor].save(commit=False)
    vendor_object.contact_person = forms[contact_person].save()
    vendor_object.bank_details = forms[bank_details].save()
    forms[vendor].save()

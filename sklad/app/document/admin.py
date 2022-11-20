from operator import xor

from django.contrib import admin

from app.document.models import DocumentNomenclatures, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'get_number', 'get_type', 'get_contactor',
        'status', 'time_create', 'time_update',
    ]
    list_display_links = ['get_number']
    list_filter = ['status']

    def get_number(self, object):
        return object.number

    get_number.short_description = 'Номер'

    def get_type(self, object):
        if xor(bool(object.vendor), bool(object.buyer)):
            return ('Отгрузка', 'Поставка')[object.buyer is None]

    get_type.short_description = 'Тип'

    def get_contactor(self, object):
        if xor(bool(object.vendor), bool(object.buyer)):
            return object.vendor or object.buyer

    get_contactor.short_description = 'Контрагент'


@admin.register(DocumentNomenclatures)
class DocumentNomenclaturesAdmin(admin.ModelAdmin):
    list_filter = ['document']
    list_display = ['document', 'nomenclature', 'amount']
    list_editable = ['nomenclature', 'amount']
    sortable_by = ['document', 'nomenclature', 'amount']

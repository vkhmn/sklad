from django.contrib import admin

from app.document.models import DocumentNomenclatures, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentNomenclatures)
class DocumentNomenclaturesAdmin(admin.ModelAdmin):
    pass

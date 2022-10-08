from django.contrib import admin
from sklad.models import *


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class DocumentAdmin(admin.ModelAdmin):
    pass

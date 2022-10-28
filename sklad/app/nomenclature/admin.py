from django.contrib import admin

from app.nomenclature.models import Nomenclature, Category, SubCategory, Store


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class DocumentAdmin(admin.ModelAdmin):
    pass

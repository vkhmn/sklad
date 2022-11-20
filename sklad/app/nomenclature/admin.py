from django.contrib import admin

from app.nomenclature.models import Nomenclature, Category, SubCategory, Store


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'article', 'subcategory', 'price']
    list_display_links = ['name']
    list_editable = ['article', 'subcategory', 'price']
    list_filter = ['subcategory']
    sortable_by = ['subcategory', 'price', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_display_links = ['name']
    list_editable = ['category']
    list_filter = ['category']


@admin.register(Store)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['nomenclature', 'amount']
    list_editable = ['amount']
    list_filter = ['amount']

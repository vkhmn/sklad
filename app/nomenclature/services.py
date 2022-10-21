from django.db.models import Count, F, Q, Sum

from .models import SubCategory, Nomenclature, Category, Store


def get_subcats():
    return SubCategory.objects.annotate(
        total=Count('nomenclature')).filter(
        total__gt=0).order_by('category__name', 'name')


def get_subcategories(category):
    return SubCategory.objects.filter(category=category)


def get_store(nomenclature):
    return Store.objects.get(nomenclature=nomenclature).amount


def get_category_total(category):
    return Store.objects.filter(
        nomenclature__in=Nomenclature.objects.filter(
            subcategory__in=get_subcategories(category)
        )).aggregate(
        sum=Sum(F('nomenclature__price') * F('amount'))
    ).get('sum')


def get_nomenclatures_list(query):
    return Nomenclature.objects.filter(name__icontains=query).annotate(
        store_amount=F('store__amount')).order_by(
        'subcategory__category__name',
        'subcategory__name',
        'name'
    )


def get_nomenclatures_category(pk, query):
    return Nomenclature.objects.filter(
        subcategory__category=pk).filter(
        name__icontains=query).annotate(
        store_amount=F('store__amount')).order_by(
        'subcategory__name',
        'name'
    )


def get_nomenclatures_subcategory(pk, query):
    return Nomenclature.objects.filter(
        Q(subcategory=pk)).filter(
        Q(name__icontains=query)).annotate(
        store_amount=F('store__amount')).order_by('name')


def get_category_name(pk):
    return Category.objects.get(pk=pk).name


def get_subcategory_name(pk):
    return SubCategory.objects.get(pk=pk).name

from django.db.models import Count, F, Q, Sum

from app.nomenclature.models import SubCategory, Nomenclature, Category, Store


class NomenclatureContext:
    """Возвращает контекст для номенклатуры."""
    @classmethod
    def _get_subcategories(cls, category):
        return SubCategory.objects.filter(category=category)

    @classmethod
    def _get_store(cls, nomenclature):
        return Store.objects.get(nomenclature=nomenclature).amount

    @classmethod
    def _get_category_total(cls, category):
        return Store.objects.filter(
            nomenclature__in=Nomenclature.objects.filter(
                subcategory__in=cls._get_subcategories(category)
            )).aggregate(
            sum=Sum(F('nomenclature__price') * F('amount'))
        ).get('sum')

    @classmethod
    def _get_category(cls, nomenclature: Nomenclature):
        return nomenclature.subcategory.category

    @classmethod
    def execute(cls, nomenclature):
        category = cls._get_category(nomenclature)
        return dict(
            subcategories=cls._get_subcategories(category),
            store=cls._get_store(nomenclature),
            total_category=cls._get_category_total(category),
        )


def get_subcats():
    return SubCategory.objects.annotate(
        total=Count('nomenclature')).filter(
        total__gt=0).order_by('category__name', 'name')


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

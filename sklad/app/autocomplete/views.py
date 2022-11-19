from dal import autocomplete
from django.db.models import Q

from app.contactor.models import Buyer
from app.nomenclature.models import SubCategory


class BuyerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Buyer.objects.select_related('person')
        if self.q:
            qs = qs.filter(person__full_name__icontains=self.q)
        return qs


class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SubCategory.objects.select_related('category')
        if self.q:
            qs = qs.filter(
               Q(name__icontains=self.q) | Q(category__name__icontains=self.q)
            )
        return qs

    def get_result_label(self, result):
        return f'{result.category} -> {result.name}'

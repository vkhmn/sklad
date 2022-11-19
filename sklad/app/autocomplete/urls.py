from dal import autocomplete
from django.urls import path

from app.autocomplete.views import BuyerAutocomplete, SubCategoryAutocomplete
from app.contactor.models import Vendor
from app.nomenclature.models import Nomenclature, Category


urlpatterns = [
    path(
        'autocomplete-nomenclature/',
        autocomplete.Select2QuerySetView.as_view(
            model=Nomenclature,
        ),
        name='autocomplete_nomenclature',
    ),
    path(
        'autocomplete-vendor/',
        autocomplete.Select2QuerySetView.as_view(
            model=Vendor,
        ),
        name='autocomplete_vendor',
    ),
    path(
        'autocomplete-subcategory/',
        SubCategoryAutocomplete.as_view(),
        name='autocomplete_subcategory',
    ),
    path(
        'autocomplete-buyer/',
        BuyerAutocomplete.as_view(),
        name='autocomplete_buyer',
    ),
    path(
        'autocomplete-category/',
        autocomplete.Select2QuerySetView.as_view(
            model=Category,
        ),
        name='autocomplete_category',
    ),
]

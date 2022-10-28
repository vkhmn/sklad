from django.urls import path

from app.nomenclature.views import (
    NomenclatureView, NomenclatureListView, NomenklatureAddView,
    CategoryView, SubCategoryView
)


urlpatterns = [
    path('nomenclature/', NomenclatureListView.as_view(),
         name='nomenclature_list'),
    path('nomenclature/add/', NomenklatureAddView.as_view(),
         name='nomenklature_add'),
    path('nomenclature/<int:pk>/', NomenclatureView.as_view(),
         name='nomenclature'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('subcategory/<int:pk>/', SubCategoryView.as_view(),
         name='subcategory'),
]

from django.urls import path

from sklad.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('add_nomenclature', AddNomenklatureView.as_view(), name='add_nomenklature'),
    path('nomenclature/', NomenclatureListView.as_view(), name='nomenclature_list'),
    path('nomenclature/<int:pk>/', NomenclatureView.as_view(), name='nomenclature'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('subcategory/<int:pk>/', SubCategoryView.as_view(), name='subcategory'),
]

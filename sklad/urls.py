from django.urls import path

from sklad.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='home'),  #
    path('login', LoginView.as_view(), name='login'),
    path('vendor/', VendorListView.as_view(), name='vendor_list'),  #
    path('vendor/add/', VendorAddView.as_view(), name='vendor_add'),  #
    path('vendor/<int:pk>/', VendorView.as_view(), name='vendor'),  #
    path('buyer/', BuyerListView.as_view(), name='buyer_list'),  #
    path('buyer/add/', BuyerAddView.as_view(), name='buyer_add'),  #
    path('buyer/<int:pk>/', BuyerView.as_view(), name='buyer'),  #
    path('shipment/', ShipmentListView.as_view(), name='shipment_list'),  #
    path('shipment/add/', ShipmentAddView.as_view(), name='shipment_add'),  #
    path('delivery/', DeliveryListView.as_view(), name='delivery_list'),  #
    path('delivery/add/', DeliveryAddView.as_view(), name='delivery_add'),  #
    path('document/<int:pk>/', DocumentView.as_view(), name='document'),  #
    path('nomenclature/', NomenclatureListView.as_view(), name='nomenclature_list'),
    path('nomenclature/add/', NomenklatureAddView.as_view(), name='nomenklature_add'),
    path('nomenclature/<int:pk>/', NomenclatureView.as_view(), name='nomenclature'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('subcategory/<int:pk>/', SubCategoryView.as_view(), name='subcategory'),
]

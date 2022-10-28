from django.urls import path

from app.contactor.views import (
    BuyerView, BuyerAddView, BuyerListView,
    VendorView, VendorAddView, VendorListView
)


urlpatterns = [
    path('vendor/', VendorListView.as_view(), name='vendor_list'),  #
    path('vendor/add/', VendorAddView.as_view(), name='vendor_add'),  #
    path('vendor/<int:pk>/', VendorView.as_view(), name='vendor'),  #
    path('buyer/', BuyerListView.as_view(), name='buyer_list'),  #
    path('buyer/add/', BuyerAddView.as_view(), name='buyer_add'),  #
    path('buyer/<int:pk>/', BuyerView.as_view(), name='buyer'),  #
]

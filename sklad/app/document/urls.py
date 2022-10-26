from django.urls import path

from .views import HomeView, ConfirmView, ChangeDocumentStatusView
from .views import ShipmentListView, ShipmentAddView
from .views import DeliveryListView, DeliveryAddView, DocumentView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shipment/', ShipmentListView.as_view(), name='shipment_list'),
    path('shipment/add/', ShipmentAddView.as_view(), name='shipment_add'),
    path('delivery/', DeliveryListView.as_view(), name='delivery_list'),
    path('delivery/add/', DeliveryAddView.as_view(), name='delivery_add'),
    path('document/<int:pk>/', DocumentView.as_view(), name='document'),
    path('document/<int:pk>/changestatus/<str:status>',
         ChangeDocumentStatusView.as_view(),
         name='document_change_status'
         ),
    path('document/confirm/', ConfirmView.as_view(), name='document_confirm'),
]

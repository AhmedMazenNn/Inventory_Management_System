from .views import *
from django.urls import path


urlpatterns = [
    path('shipment/',list_shipment, name='shipment_list'),
    path('shipment/<int:pk>',shipment_detail, name='shipment_detail'),
    path('shipment/create',create_shipment, name='create_shipment'),
    path('shipment/update/<int:pk>',update_shipment, name='update_shipment'),
]
app_name = 'shipment'
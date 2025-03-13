from .views import *
from django.urls import path

urlpatterns = [
    path('shipment/<int:pk>', shipment_detail, name='shipment_detail'),
    path('shipment/create', create_shipment, name='create_shipment'),
    path('shipment/update/<int:pk>', update_shipment, name='update_shipment'),
]

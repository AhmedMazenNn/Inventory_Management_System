from .views import *
from . import views
from django.urls import path

urlpatterns = [
    path('shipment/', views.list_shipment, name='shipment_list'),
    path('shipment/<int:pk>', views.shipment_detail, name='shipment_detail'),
    path('shipment/create', views.create_shipment, name='create_shipment'),
    path('shipment/update/<int:pk>', views.update_shipment, name='update_shipment'),
]

from django.urls import path
from .views import * 

urlpatterns =[
    path("home/",home_page,name="home"),
    path("search/",search_product,name="search"),
    path("list_all/",List_all_products.as_view(),name="list_all"),
    path("update_product/<int:pk>/", Update_product.as_view(), name="update_product"),
    path("add_product/",create_product.as_view(),name="add_product"),
]
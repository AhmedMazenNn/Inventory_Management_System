from django.urls import path
from .views import (
    OrderListView, OrderDetailView, OrderCreateView, OrderItemCreateView,
    OrderUpdateView, OrderApproveView, OrderDeleteView, approve_order
)

app_name = "orders"

urlpatterns = [
    path("all_orders/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("create/", OrderCreateView.as_view(), name="create_order"),
    path("add-item/<int:order_id>/", OrderItemCreateView.as_view(), name="add_order_item"),
    path("<int:order_id>/approve/", approve_order, name="approve_order"),
    path("update-item/<int:pk>/", OrderUpdateView.as_view(), name="update_order_item"),  # ✅ تصحيح هنا
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="delete_order"),
]
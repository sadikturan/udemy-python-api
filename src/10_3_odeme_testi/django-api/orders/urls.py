from django.urls import path
from .views import OrderListView, OrderDetailsView, OrderCreateView, AdminOrderListView, AdminOrderDetailsView, AdminOrderStatusUpdateView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>', OrderDetailsView.as_view(), name='order_details'),
    path('create', OrderCreateView.as_view(), name='order_create'),
    path('admin', AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/<int:pk>/', AdminOrderDetailsView.as_view(), name='admin_order_details'),
    path('admin/<int:pk>/update-status', AdminOrderStatusUpdateView.as_view(), name='admin_order_status_update'),
]

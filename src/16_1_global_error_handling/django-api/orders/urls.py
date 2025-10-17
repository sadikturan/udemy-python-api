from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create', views.CreateOrderView.as_view(), name='order_create'),
    path('admin', views.AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/<int:order_id>', views.AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('<int:order_id>', views.OrderDetailView.as_view(), name='order_detail'),
]

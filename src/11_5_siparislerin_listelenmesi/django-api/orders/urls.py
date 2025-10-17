from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('admin', views.AdminOrderListView.as_view(), name='admin_order_list'),
    path('create', views.CreateOrderView.as_view(), name='order_create'),
]

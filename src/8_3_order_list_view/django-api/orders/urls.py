from django.urls import path
from .views import CreateOrderView, CreateListView, CreateDetailsView

urlpatterns = [
    path('', CreateListView.as_view(), name='order_list'),
    path('<int:pk>', CreateDetailsView.as_view(), name='order_details'),
    path('create', CreateOrderView.as_view(), name='order_create'),
]

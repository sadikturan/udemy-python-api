from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddressListView.as_view(), name='address_list'),
    path('<int:address_id>', views.AddressDetailView.as_view(), name='address_update'),

    path('admin/<int:user_id>', views.AdminAddressListView.as_view(), name='admin_address_list'),
    path('admin/detail/<int:address_id>', views.AdminAddressDetailView.as_view(), name='admin_address_update'),
]

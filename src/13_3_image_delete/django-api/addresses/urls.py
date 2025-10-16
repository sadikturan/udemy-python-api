from django.urls import path
from .views import AddressListView, AddressCreateView, AddressDetailsView, AddressUpdateView, AddressDeleteView, AdminAddressListView, AdminAddressCreateView, AdminAddressDetailsView, AdminAddressUpdateView, AdminAddressDeleteView

urlpatterns = [
    path('', AddressListView.as_view(), name="address_list_view"),
    path('create', AddressCreateView.as_view(), name="address_create_view"),
    path('<int:pk>', AddressDetailsView.as_view(), name="address_details_view"),
    path('<int:pk>/update', AddressUpdateView.as_view(), name="address_update_view"),
    path('<int:pk>/delete', AddressDeleteView.as_view(), name="address_delete_view"),
    path('admin', AdminAddressListView.as_view(), name="address_list_view"),
    path('admin/create', AdminAddressCreateView.as_view(), name="address_create_view"),
    path('admin/<int:pk>', AdminAddressDetailsView.as_view(), name="address_details_view"),
    path('admin/<int:pk>/update', AdminAddressUpdateView.as_view(), name="address_update_view"),
    path('admin/<int:pk>/delete', AdminAddressDeleteView.as_view(), name="address_delete_view"),
]
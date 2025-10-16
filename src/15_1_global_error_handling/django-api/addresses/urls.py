from django.urls import path
from .views import AddressListCreateView, AddressDetailUpdateDeleteView, AdminAddressListCreateView, AdminAddressRetrieveUpdateDeleteView

urlpatterns = [
    path('', AddressListCreateView.as_view(), name="address_list_create_view"),
    path('<int:address_id>', AddressDetailUpdateDeleteView.as_view(), name="address_details_update_delete_view"),
    path('admin', AdminAddressListCreateView.as_view(), name="address_list_create_view"),
    path('admin/<int:address_id>', AdminAddressRetrieveUpdateDeleteView.as_view(), name="address_details_view"),
]
from django.urls import path
from .views import AddressListView, AddressCreateView, AddressDetailsView, AddressUpdateView, AddressDeleteView

urlpatterns = [
    path('', AddressListView.as_view(), name="address_list_view"),
    path('create', AddressCreateView.as_view(), name="address_create_view"),
    path('<int:pk>', AddressDetailsView.as_view(), name="address_details_view"),
    path('<int:pk>/update', AddressUpdateView.as_view(), name="address_update_view"),
    path('<int:pk>/delete', AddressDeleteView.as_view(), name="address_delete_view"),
]
from django.urls import path
from .views import AddressListView, AddressCreateView, AddressDetailsView

urlpatterns = [
    path('', AddressListView.as_view(), name="address_list_view"),
    path('create', AddressCreateView.as_view(), name="address_create_view"),
    path('<int:pk>', AddressDetailsView.as_view(), name="address_details_view"),
]
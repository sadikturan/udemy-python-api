from django.urls import path
from .views import AddressListView

urlpatterns = [
    path('', AddressListView.as_view(), name="address_list_view"),
]
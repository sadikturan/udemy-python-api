from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import AddressListSerializer, AddressCreateSerializer, AddressDetailsSerializer
from .services import get_user_addresses, set_default_address

class AddressListView(generics.ListAPIView):
    serializer_class = AddressListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)
    
class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        address = serializer.save(user = self.request.user)
        if address.is_default:
            set_default_address(address)

class AddressDetailsView(generics.RetrieveAPIView):
    serializer_class = AddressDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)

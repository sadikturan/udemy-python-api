from rest_framework import generics, permissions
from .models import Address
from . import serializers

class AddressListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.AddressCreateUpdateSerializer
        return serializers.AddressSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "address_id"

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.AddressDetailSerializer
        return serializers.AddressCreateUpdateSerializer
    
    
class AdminAddressListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Address.objects.filter(user=user_id)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.AddressCreateUpdateSerializer
        return serializers.AddressSerializer
    
    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        serializer.save(user=user_id)

class AdminAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = "address_id"

    def get_queryset(self):
        return Address.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.AddressDetailSerializer
        return serializers.AddressCreateUpdateSerializer




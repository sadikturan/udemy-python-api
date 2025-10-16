from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import AddressListSerializer, AddressSerializer, AddressDetailsSerializer
from .services import get_user_addresses, set_default_address
from .models import Address
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AddressListView(generics.ListAPIView):
    serializer_class = AddressListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        address = serializer.save(user = self.request.user)
        if address.is_default:
            set_default_address(address)

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AddressDetailsView(generics.RetrieveAPIView):
    serializer_class = AddressDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AddressUpdateView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)
    
    def perform_update(self, serializer):
        address = serializer.save()
        if address.is_default:
            set_default_address(address)

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
) 
class AdminAddressListView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)  
class AdminAddressCreateView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AdminAddressDetailsView(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressDetailsSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)    
class AdminAddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(
    summary="Kullanıcı Adresleri",
    description="Auth olan kullanıcının adres listesini getirir.",
    tags=['Addresses']
)
class AdminAddressDeleteView(generics.DestroyAPIView):
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAdminUser]
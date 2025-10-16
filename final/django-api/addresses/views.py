from rest_framework import generics, permissions
from .models import Address
from . import serializers
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(
        summary="Adres Listesi",
        description="Auth olan kullanıcının adres listesini getirir.",
        tags=["Address"],
        responses=serializers.AddressSerializer(many=True)
    ),
    post=extend_schema(
        summary="Adres Ekle",
        description="Auth olan kullanıcı için yeni adres ekler.",
        tags=["Address"],
        request=serializers.AddressCreateUpdateSerializer,
        responses=serializers.AddressSerializer
    )
)
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

@extend_schema_view(
    get=extend_schema(
        summary="Adres Detayları",
        description="Auth olan kullanıcının seçilen adres detaylarını getirir.",
        tags=["Address"],
        responses=serializers.AddressDetailSerializer
    ),
    put=extend_schema(
        summary="Adres Güncelle",
        description="Auth olan kullanıcının adresini günceller.",
        tags=["Address"],
        request=serializers.AddressCreateUpdateSerializer,
        responses=serializers.AddressDetailSerializer
    ),
    patch=extend_schema(
        summary="Adres Güncelle (Kısmi)",
        description="Auth olan kullanıcının adresinin bazı alanlarını günceller.",
        tags=["Address"],
        request=serializers.AddressCreateUpdateSerializer,
        responses=serializers.AddressDetailSerializer,
    ),
    delete=extend_schema(
        summary="Adres Sil",
        description="Auth olan kullanıcının adresini siler.",
        tags=["Address"]
    ),
)
class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "address_id"

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.AddressDetailSerializer
        return serializers.AddressCreateUpdateSerializer
    
@extend_schema_view(
    get=extend_schema(
        summary="Tüm Kullanıcı Adresleri (Admin)",
        description="Admin, tüm kullanıcı adreslerini listeleyebilir.",
        tags=["Address"],
        responses=serializers.AddressSerializer
    ),
    post=extend_schema(
        summary="Yeni Adres Oluştur (Admin)",
        description="Admin, yeni bir kullanıcı adresi oluşturabilir.",
        tags=["Address"],
        request=serializers.AddressCreateUpdateSerializer,
        responses=serializers.AddressSerializer
    ),
)
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

@extend_schema_view(
    get=extend_schema(
        summary="Adres Detayları",
        description="Auth olan kullanıcının seçilen adres detaylarını getirir.",
        tags=["Address"],
        responses=serializers.AddressDetailSerializer
    ),
    put=extend_schema(
        summary="Adres Güncelle",
        description="Auth olan kullanıcının adresini günceller.",
        tags=["Address"],
        request=serializers.AddressCreateUpdateSerializer,
        responses=serializers.AddressDetailSerializer
    ),
    patch=extend_schema(
        summary="Adres Güncelle (Kısmi)",
        description="Auth olan kullanıcının adresinin bazı alanlarını günceller.",
        tags=["Address"],
        request=serializers.AddressCreateUpdateSerializer,
        responses=serializers.AddressDetailSerializer,
    ),
    delete=extend_schema(
        summary="Adres Sil",
        description="Auth olan kullanıcının adresini siler.",
        tags=["Address"]
    ),
)
class AdminAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = "address_id"

    def get_queryset(self):
        return Address.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.AddressDetailSerializer
        return serializers.AddressCreateUpdateSerializer




from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import AddressListSerializer, AddressSerializer, AddressDetailsSerializer, AddressSerializer, AddressListSerializer
from .services import get_user_addresses, set_default_address
from .models import Address

@extend_schema_view(
    get=extend_schema(
        summary="Adres Listesi",
        description="Auth olan kullanıcının adres listesini getirir.",
        tags=["Addresses"],
        responses=AddressListSerializer(many=True)
    ),
    post=extend_schema(
        summary="Adres Ekle",
        description="Auth olan kullanıcı için yeni adres ekler.",
        tags=["Addresses"],
        request=AddressSerializer,
        responses=AddressSerializer
    )
)
class AddressListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "address_id"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddressSerializer
        return AddressListSerializer

    def get_queryset(self):
        return get_user_addresses(self.request.user)

    def perform_create(self, serializer):
        address = serializer.save(user=self.request.user)
        if address.is_default:
            set_default_address(address)


@extend_schema_view(
    get=extend_schema(
        summary="Adres Detayları",
        description="Auth olan kullanıcının seçilen adres detaylarını getirir.",
        tags=["Addresses"],
        responses=AddressDetailsSerializer
    ),
    put=extend_schema(
        summary="Adres Güncelle",
        description="Auth olan kullanıcının adresini günceller.",
        tags=["Addresses"],
        request=AddressSerializer,
        responses=AddressSerializer
    ),
    patch=extend_schema(
        summary="Adres Güncelle (Kısmi)",
        description="Auth olan kullanıcının adresinin bazı alanlarını günceller.",
        tags=["Addresses"],
        request=AddressSerializer,
        responses=AddressSerializer
    ),
    delete=extend_schema(
        summary="Adres Sil",
        description="Auth olan kullanıcının adresini siler.",
        tags=["Addresses"]
    ),
)
class AddressDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "address_id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AddressDetailsSerializer
        return AddressSerializer

    def get_queryset(self):
        return get_user_addresses(self.request.user)

    def perform_update(self, serializer):
        address = serializer.save()
        if address.is_default:
            set_default_address(address)

@extend_schema_view(
    get=extend_schema(
        summary="Tüm Kullanıcı Adresleri (Admin)",
        description="Admin, tüm kullanıcı adreslerini listeleyebilir.",
        tags=["Addresses"],
        responses=AddressListSerializer
    ),
    post=extend_schema(
        summary="Yeni Adres Oluştur (Admin)",
        description="Admin, yeni bir kullanıcı adresi oluşturabilir.",
        tags=["Addresses"],
        request=AddressSerializer,
        responses=AddressSerializer
    ),
)
class AdminAddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = "address_id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AddressListSerializer
        return AddressSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Adres Detay (Admin)",
        description="Admin kullanıcı bir adresin detaylarını görüntüler.",
        tags=["Addresses"],
        responses=AddressDetailsSerializer
    ),
    put=extend_schema(
        summary="Adres Güncelleme (Admin)",
        description="Admin kullanıcı bir adresi günceller.",
        tags=["Addresses"],
        request=AddressSerializer,
        responses=AddressSerializer
    ),
    patch=extend_schema(
        summary="Adres Güncelleme (Admin - PATCH)",
        description="Admin kullanıcı bir adresi PATCH ile kısmen günceller.",
        tags=["Addresses"],
        request=AddressSerializer,
        responses=AddressSerializer
    ),
    delete=extend_schema(
        summary="Adres Silme (Admin)",
        description="Admin kullanıcı bir adresi siler.",
        tags=["Addresses"]
    ),
)
class AdminAddressRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = "address_id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AddressDetailsSerializer
        return AddressSerializer
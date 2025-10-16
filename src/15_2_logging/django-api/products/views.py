import os
import shutil
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from core.paginations import StandardResultsSetPagination
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductListSerializer, ProductDetailsSerializer, ProductImageUploadSerializer, ProductImageSerializer
from .services import get_product_or_404
from .filters import ProductFilter

@extend_schema(
    summary="Stokta olan ürünlerin listesi",
    description="Stok miktarı 0'dan büyük olan ürünleri listeler. Filtreleme, arama ve sıralama desteklenir.",
    tags=['Products'],
)
class CatalogProductList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(stock__gt = 0)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
    ordering = ['-id']

@extend_schema_view(
    get=extend_schema(
        summary="Ürün görsellerini listele",
        description="Belirtilen ürünün görsellerini listeler.",
        responses=ProductImageSerializer(many=True),
        tags=['Products']
    ),
    post=extend_schema(
        summary="Ürün görseli yükle",
        description="Belirtilen ürüne yeni bir görsel yükler.",
        request=ProductImageUploadSerializer,
        responses=ProductImageSerializer,
        tags=['Products']
    )
)
class ProductImages(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductImageUploadSerializer
        return ProductImageSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        return ProductImage.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        product = get_product_or_404(product_id)
        serializer.save(product=product)

@extend_schema(
    summary="Ürün görselini sil",
    description="Belirtilen ürün görselini siler ve ilişkili dosyayı da depolamadan kaldırır.",
    tags=['Products']
)
class ProductImageDelete(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.image:
            instance.image.delete(save=False)
        instance.delete()

        return Response({'message': 'Image deleted.'}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    summary="Catalog: Ürün detaylarını ID ile al",
    description="Verilen ID'ye sahip ürünün detaylarını döner.",
    tags=['Products'],
    responses=ProductDetailsSerializer
)
class CatalogProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer

@extend_schema(
    summary="Admin: Tüm ürünleri listele",
    description="Yalnızca admin kullanıcıların erişebileceği, tüm ürünleri listeleyen endpoint.",
    tags=['Products'],
    responses=ProductListSerializer(many=True)
)
class AdminProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    summary="Admin: Ürün detaylarını ID ile al",
    description="Yalnızca admin kullanıcıların erişebileceği, verilen ID'ye sahip ürünün detaylarını döner.",
    tags=['Products'],
    responses=ProductDetailsSerializer
)
class AdminProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Admin: Ürün oluştur",
    description="Yalnızca admin kullanıcıların erişebileceği, yeni ürün oluşturma endpoint'i.",
    tags=['Products'],
    request=ProductSerializer,
    responses=ProductSerializer
)
class AdminCreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Admin: Ürün güncelle",
    description="Yalnızca admin kullanıcıların erişebileceği, belirtilen ürünü günceller.",
    tags=['Products'],
    request=ProductSerializer,
    responses=ProductSerializer
)
class AdminEditProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    
@extend_schema(
    summary="Admin: Ürünü sil",
    description="Belirtilen ürünü, ilişkili tüm görselleri ve ürün klasörünü siler.",
    responses={204: None},
    tags=['Products']
)
class AdminDeleteProduct(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object() 

        images = ProductImage.objects.filter(product = product)

        for img in images:
            if img.image:
                img.image.delete(save=False)
            img.delete()

        product_folder = os.path.join(settings.MEDIA_ROOT, 'products', str(product.id))

        if os.path.exists(product_folder):
            shutil.rmtree(product_folder)

        product.delete()
        return Response({'message': 'Product and related images (and folder) deleted.'}, status=status.HTTP_204_NO_CONTENT)
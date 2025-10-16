import os
import shutil
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from core.pagination import StandardResultsSetPagination
from . import serializers
from .models import Product, ProductImage
from .throttles import ProductListThrottle
from .filters import ProductFilter
from .services import get_product_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from core.permissions import HasValidAPIKey, IsAdminWithAPIKey
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics, filters
from rest_framework.permissions import  IsAdminUser

@extend_schema(
    summary="Ürün Listesi",
    description=(
        "Aktif ürünlerin listesini döner."
        "Filtreleme, arama ve sıralama desteği sunar.\n\n"
        "**Filtreleme parametreleri:**\n"
        "- `name__iexact`: Ürün adını tam (büyük/küçük harf duyarsız) eşleştirir\n"
        "- `name__icontains`: Ürün adında geçen kelimeyi arar\n"
        "- `price__lt`: Belirtilen değerden düşük fiyatlı ürünler\n"
        "- `price__gt`: Belirtilen değerden yüksek fiyatlı ürünler\n"
        "- `price__range`: Örnek: `?price__range=100,500`\n\n"
        "**Arama:** `?search=iphone`\n\n"
        "**Sıralama:** `?ordering=price` veya `?ordering=-price`\n"
    ),
    tags=["Product"],
    parameters=[
        OpenApiParameter(name='q', description='Ürün adı veya açıklamasında arama yapar', required=False, type=str),
        OpenApiParameter(name='ordering', description='Sıralama alanı (`price`, `name`, `-price`, `-name`)', required=False, type=str),
        OpenApiParameter(name='name__iexact', description='Ürün adını tam (büyük/küçük harf duyarsız) eşleştirir', required=False, type=str),
        OpenApiParameter(name='name__icontains', description='Ürün adında geçen kelimeyi arar', required=False, type=str),
        OpenApiParameter(name='price__lt', description='Belirtilen değerden düşük fiyatlı ürünleri getirir', required=False, type=OpenApiTypes.NUMBER),
        OpenApiParameter(name='price__gt', description='Belirtilen değerden yüksek fiyatlı ürünleri getirir', required=False, type=OpenApiTypes.NUMBER),
        OpenApiParameter(name='price__range', description='Belirtilen fiyat aralığındaki ürünleri getirir. Örnek: `100,500`', required=False, type=str),
        OpenApiParameter(name='page', description='Sayfa numarası', required=False, type=int),
        OpenApiParameter(name='page_size', description='Sayfa başına öğe sayısı (varsayılan: 10)', required=False, type=int),
    ]
)
class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(isActive=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
    ordering = ['-id']
    throttle_classes = [ProductListThrottle]
    # permission_classes = [HasValidAPIKey]

@extend_schema_view(
    get=extend_schema(
        summary="Ürün görsellerini listele",
        description=(
            "Belirtilen ürünün tüm görsellerini listeler.\n\n"
            "**Yalnızca admin kullanıcılar erişebilir.**"
        ),
        tags=["Product"],
        responses={
            200: serializers.ProductImageSerializer(many=True)
        },
        examples=[
            OpenApiExample(
                name= "Listeleme Örneği",
                summary="Ürün görselleri listesi",
                value=[
                    {
                        "id": 1,
                        "product": 12,
                        "image": "http://127.0.0.1:8000/media/products/image1.jpg",
                    },
                    {
                        "id": 2,
                        "product": 12,
                        "image": "http://127.0.0.1:8000/media/products/image2.jpg",
                    },
                ],
            )
        ],
    ),
    post=extend_schema(
        summary="Yeni ürün görseli yükle",
        description=(
            "Belirtilen ürüne yeni bir görsel yükler.\n\n"
            "**Sadece admin kullanıcılar** bu işlemi yapabilir.\n\n"
            "Yükleme `multipart/form-data` formatında yapılmalıdır."
        ),
        tags=["Product"],
        request={
            "multipart/form-data": serializers.ProductImageSerializer
        }, 
        responses={
            201: serializers.ProductImageSerializer
        },
        examples=[
            OpenApiExample(
                name="Başarılı Yükleme Yanıtı",
                summary="Başarılı görsel yükleme örneği",
                value={
                    "id": 5,
                    "product": 12,
                    "image": "http://127.0.0.1:8000/media/products/new_image.jpg",
                },
                response_only=True,
            ),
        ]

    ),
)
class ProductImages(generics.ListCreateAPIView):
    permission_classes = [IsAdminWithAPIKey]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.ProductImageUploadSerializer
        return serializers.ProductImageSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        return ProductImage.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("pk")
        product = get_product_or_404(product_id)
        serializer.save(product=product)

@extend_schema(
    summary="Ürün görselini sil",
    description="Belirtilen ürün görselini siler ve ilişkili dosyayı da depolamadan kaldırır.",
    tags=['Product']
)
class ProductImageDelete(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.image:
            instance.image.delete(save=False)
        
        instance.delete()

        return Response({"message": "Image deleted."}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    summary="Admin: Tüm ürünleri listele",
    description="Yalnızca admin kullanıcıların erişebileceği, tüm ürünleri listeler ve ayrıca kategory filtresi uygular.",
    tags=['Product'],
    responses=serializers.AdminProductSerializer(many=True)
)
class AdminProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.AdminProductSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Ürün detaylarını ID ile al",
    description="Verilen ID'ye sahip ürünün detaylarını döner.",
    tags=['Product'],
    responses=serializers.ProductDetailSerializer
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer

    def get_object(self):
        return get_product_or_404(self.kwargs["pk"])

@extend_schema(
    summary="Admin: Ürün detaylarını ID ile al",
    description="Yalnızca admin kullanıcıların erişebileceği, verilen ID'ye sahip ürünün detaylarını döner.",
    tags=['Product'],
    responses=serializers.AdminProductDetailSerializer
)
class AdminProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.AdminProductDetailSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Admin: Ürün oluştur",
    description="Yalnızca admin kullanıcıların erişebileceği, yeni ürün oluşturma endpoint'i.",
    tags=['Product'],
    request=serializers.ProductCreateSerializer,
    responses=serializers.ProductCreateSerializer
)
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductCreateSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Ürün güncelleme",
    description="Belirtilen ürünü günceller.",
    request=serializers.ProductUpdateSerializer,
    tags=['Product']
)
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductUpdateSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Ürün silme",
    description="Belirtilen ürünü, ilişkili tüm görselleri ve ürün klasörünü siler.",
    responses={204: None},
    tags=['Product']
)
class DeleteProduct(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()

        images = ProductImage.objects.filter(product=product)

        for img in images:
            if img.image:
                img.image.delete(save=False)
            img.delete()

        product_folder = os.path.join(settings.MEDIA_ROOT, "products", str(product.id))

        if os.path.exists(product_folder):
            shutil.rmtree(product_folder)

        product.delete()

        return Response({"message": "Ürün ve ürün resimleri silindi."}, status=status.HTTP_204_NO_CONTENT)





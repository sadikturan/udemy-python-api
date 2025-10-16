from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Category
from .serializers import CategorySerializer, CategoryListSerializer, CategoryDetailsSerializer

@extend_schema(
    responses=CategoryListSerializer(many=True),
    summary="Kategori Listesi",
    description="Onaylı olan tüm kategorileri getirir.",
    tags=["Categories"]
)
class CatalogCategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

@extend_schema(
    responses=CategoryDetailsSerializer,
    summary="Kategori Detayı",
    description="Belirli bir kategorinin detayını getirir.",
    tags=["Categories"]
)
class CatalogCategoryDetails(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailsSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Kategorileri Listele",
        description="Tüm kategorileri listeler (sadece admin erişimi).",
        responses=CategoryListSerializer(many=True),
        tags=["Categories"],
    ),
    post=extend_schema(
        summary="Yeni Kategori Oluştur",
        description="Yeni bir kategori oluşturur (sadece admin erişimi).",
        request=CategorySerializer,
        responses=CategorySerializer,
        tags=["Categories"],
    )
)
class AdminCategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategorySerializer
        return CategoryListSerializer
 
@extend_schema_view(
    get=extend_schema(
        summary="Kategori Detayı (Admin)",
        description="Belirli bir kategorinin detayını getirir (admin erişimi gereklidir).",
        responses=CategoryDetailsSerializer,
        tags=["Categories"]
    ),
    put=extend_schema(
        summary="Kategori Güncelle (PUT, Admin)",
        description="Kategori bilgilerini tamamen günceller (admin).",
        request=CategorySerializer,
        responses=CategorySerializer,
        tags=["Categories"]
    ),
    patch=extend_schema(
        summary="Kategori Güncelle (PATCH, Admin)",
        description="Kategori bilgisini kısmen günceller (admin erişimi gereklidir).",
        request=CategorySerializer,
        responses=CategorySerializer,
        tags=["Categories"]
    ),
    delete=extend_schema(
        summary="Kategori Sil (Admin)",
        description="Kategori silme işlemi gerçekleştirir (admin erişimi gereklidir).",
        tags=["Categories"]
    )
)
class AdminCategoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryDetailsSerializer
        return CategorySerializer
    
    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        # İlişkili ürün var mı kontrolü
        if category.products.exists():
            return Response(
                {"detail": "Bu kategoriye bağlı ürünler olduğu için silinemez."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)
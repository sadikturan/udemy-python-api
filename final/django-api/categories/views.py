from . import serializers
from .models import Category
from core.permissions import IsAdminOrReadOnly
from core.pagination import StandardResultsSetPagination
from django.db.models.deletion import RestrictedError
from rest_framework import status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(
        summary="Kategorileri Listele",
        description="Tüm kategorileri listeler.",
        responses=serializers.CategorySerializer(many=True),
        tags=["Category"],
    ),
    post=extend_schema(
        summary="Yeni Kategori Oluştur",
        description="Yeni bir kategori oluşturur",
        request=serializers.CategoryCreateUpdateSerializer,
        responses=serializers.CategorySerializer,
        tags=["Category"],
    )
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CategoryCreateUpdateSerializer
        return serializers.CategorySerializer
    
@extend_schema_view(
    get=extend_schema(
        summary="Kategori Detayı",
        description="Belirtilen ID’ye sahip kategorinin detayını döner.",
        responses=serializers.CategoryDetailSerializer,
        tags=["Category"],
    ),
    put=extend_schema(
        summary="Kategoriyi Güncelle (PUT)",
        description="Kategoriyi tamamen günceller (tüm alanlar zorunlu).",
        request=serializers.CategoryCreateUpdateSerializer,
        responses=serializers.CategoryDetailSerializer,
        tags=["Category"],
    ),
    patch=extend_schema(
        summary="Kategoriyi Güncelle (PATCH)",
        description="Kategorinin bir veya birkaç alanını kısmi olarak günceller.",
        request=serializers.CategoryCreateUpdateSerializer,
        responses=serializers.CategoryDetailSerializer,
        tags=["Category"],
    ),
    delete=extend_schema(
        summary="Kategoriyi Sil",
        description="Belirtilen kategoriyi siler. Eğer bu kategoriye ait ürünler varsa silme işlemi engellenir.",
        responses={204: {"message": "Category deleted"}, 400: {"error": "Bu kategoride ürünler var. Silinemez."}},
        tags=["Category"],
    ),
)
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CategoryCreateUpdateSerializer
        return serializers.CategoryDetailSerializer
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()

        try:
            category.delete()
            return Response({"message":"Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        except RestrictedError:
            return Response({"error": "Bu kategoride ürünler var. Silinemez. Önce ürünleri siliniz."}, status=status.HTTP_400_BAD_REQUEST)
        


    

    


        
     

        



    



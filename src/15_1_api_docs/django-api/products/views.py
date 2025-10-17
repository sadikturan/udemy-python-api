from rest_framework.response import Response
from .models import Product, ProductImage
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics, filters
from  rest_framework.permissions import  IsAdminUser
from core.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .services import get_product_or_404
import os
import shutil
from django.conf import settings

class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(isActive=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
    ordering = ['-id']

class ProductImages(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

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

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_product_list(request):
    products = Product.objects.all()
    serializer = serializers.AdminProductSerializer(products, many=True) 
    return Response(serializer.data)

@api_view(['GET'])
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = serializers.ProductDetailSerializer(product)    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_product_details(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = serializers.AdminProductDetailSerializer(product)    
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def product_create(request):
    serializer = serializers.ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    try:
        product =  Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = serializers.ProductUpdateSerializer(product, data=request.data)
    else:
        serializer = serializers.ProductUpdateSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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





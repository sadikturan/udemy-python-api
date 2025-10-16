from .models import Product
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer, ProductListSerializer, ProductDetailsSerializer
from .services import get_product_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from core.paginations import LargeResultsSetPagination, StandardResultsSetPagination

@api_view(['GET'])
def catalog_list_products(request):
    """Catalog: List all products"""
    queryset = Product.objects.filter(stock__gt = 0)

    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ProductListSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def catalog_list_products_by_catid(request, pk):
    """Catalog: List all products By Category Id"""
    products = Product.objects.filter(category = pk)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def catalog_product_details(request,pk):
    """Catalog: Get Product Details By Id"""
    product = get_product_or_404(pk)
    serializer = ProductDetailsSerializer(product)
    return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_products(request):
    """Admin: List all products"""
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_product_details(request,pk):
    """Admin: Get Product Details By Id"""
    product = get_product_or_404(pk)    
    serializer = ProductDetailsSerializer(product)
    return Response(serializer.data)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_product(request):
    """Admin: Create Product"""
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_edit_product(request,pk):
    """Admin: Update Product"""
    product = get_product_or_404(pk)
    serializer = ProductSerializer(product,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_product(request,pk):
    """Admin: Delete Product"""
    product = get_product_or_404(pk)
    product.delete()
    return Response({'message': 'Product deleted.'}, status=status.HTTP_204_NO_CONTENT)
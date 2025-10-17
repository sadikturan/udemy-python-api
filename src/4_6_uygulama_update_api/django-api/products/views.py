from rest_framework.response import Response
from django.shortcuts import render
from .models import Product
from . import serializers
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = serializers.ProductSerializer(products, many=True) 
    return Response(serializer.data)

@api_view(['GET'])
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = serializers.ProductDetailSerializer(product)    
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    serializer = serializers.ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
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



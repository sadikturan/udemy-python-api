from rest_framework.response import Response
from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer, ProductCreateSerializer
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data)

@api_view(['GET'])
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductDetailSerializer(product)    
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    serializer = ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


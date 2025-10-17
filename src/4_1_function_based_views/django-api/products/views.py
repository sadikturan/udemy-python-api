from rest_framework.response import Response
from django.shortcuts import render
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True) 
    return Response(serializer.data)

@api_view(['GET'])
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductDetailSerializer(product)    
    return Response(serializer.data)

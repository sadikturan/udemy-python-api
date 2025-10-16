from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from rest_framework.response import Response

@api_view()
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view()
def product_details(request,pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
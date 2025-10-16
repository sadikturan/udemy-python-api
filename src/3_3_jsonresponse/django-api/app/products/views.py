from django.shortcuts import render
from .models import Product
from django.http import JsonResponse

def product_list(request):
    products = Product.objects.all()
    data = {
        'products': list(products.values())
    }
    return JsonResponse(data)
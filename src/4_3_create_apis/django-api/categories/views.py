from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer
from  rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request,pk):
    category = Category.objects.get(pk=pk)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)

    



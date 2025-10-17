from rest_framework import status
from .models import Category
from . import serializers
from  rest_framework.response import Response
from rest_framework.decorators import api_view

# / categories
# / categories/create

@api_view(['GET','POST'])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":    
        serializer = serializers.CategoryCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','PATCH'])
def category_detail(request,pk):
    if request.method == "GET":
        category = Category.objects.get(pk=pk)
        serializer = serializers.CategoryDetailSerializer(category)
        return Response(serializer.data)
    
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return  Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer  = serializers.CategoryCreateUpdateSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PATCH":
        serializer  = serializers.CategoryCreateUpdateSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     

        



    



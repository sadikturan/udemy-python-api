from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer, CategoryListSerializer, CategoryDetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

class CatalogCategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many = True)
        return Response(serializer.data)
        
class AdminCategoryList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many = True)
        return Response(serializer.data)
    
class CatalogCategoryDetails(APIView):

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'Error': 'Category not found'}, status=404)
        serializer = CategoryDetailsSerializer(category)
        return Response(serializer.data)
 
class AdminCategoryDetails(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'Error': 'Category not found'}, status=404)
        serializer = CategoryDetailsSerializer(category)
        return Response(serializer.data)
    
class AdminCategoryCreate(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AdminCategoryEdit(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class AdminCategoryDelete(APIView):
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'Error': 'Category not found'}, status=404)
        category.delete()
        return Response({'message': 'Category deleted.'}, status=status.HTTP_204_NO_CONTENT)

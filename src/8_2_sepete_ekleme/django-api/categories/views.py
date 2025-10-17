from .models import Category
from . import serializers
from django.db.models.deletion import RestrictedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from  rest_framework.permissions import IsAdminUser
from core.permissions import IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CategoryCreateUpdateSerializer
        return serializers.CategorySerializer
    

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CategoryCreateUpdateSerializer
        return serializers.CategoryDetailSerializer
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()

        try:
            category.delete()
            return Response({"message":"Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        except RestrictedError:
            return Response({"error": "Bu kategoride ürünler var. Silinemez. Önce ürünleri siliniz."}, status=status.HTTP_400_BAD_REQUEST)
        


    

    


        
     

        



    



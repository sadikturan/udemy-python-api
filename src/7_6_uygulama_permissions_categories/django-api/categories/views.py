from .models import Category
from . import serializers
from django.db.models.deletion import RestrictedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from  rest_framework.permissions import IsAdminUser

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CategoryCreateUpdateSerializer
        return serializers.CategorySerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return super().get_permissions()
    

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()

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
        
    def get_permissions(self):
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [IsAdminUser()]
        return super().get_permissions()


    

    


        
     

        



    



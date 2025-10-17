from rest_framework import serializers
from .models import Product
# from categories.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source="category.name")
    # category = CategorySerializer()
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price","category"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        exclude = ["isHome","isActive"]
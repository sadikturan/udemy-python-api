from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price","category"]

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ["name", "slug", "price","category", "description"]

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ["name", "description", "slug", "stock", "price","category","isHome","isActive" ]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        exclude = ["isHome","isActive"]
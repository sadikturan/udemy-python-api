from .models import Category
from rest_framework import serializers
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ["id","name", "slug", "icon"]

class CategoryDetailSerializer(serializers.ModelSerializer):
    # products = serializers.StringRelatedField(many=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id","name", "slug", "icon", "description","products"]
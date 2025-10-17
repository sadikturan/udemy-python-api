from rest_framework import serializers

class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    isHome = serializers.BooleanField()
    isActive = serializers.BooleanField()
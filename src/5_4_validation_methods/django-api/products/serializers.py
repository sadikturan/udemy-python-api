from rest_framework import serializers
from .models import Product
from categories.models import Category
from . import validations

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price","category"]

class ProductCreateSerializer(serializers.ModelSerializer):

    isHome = serializers.BooleanField(required=False)
    isActive = serializers.BooleanField(required=False)

    stock = serializers.IntegerField(
        min_value=0,
        required=False,
        error_messages  = {
            "min_value": "Stok negatif değer olamaz."
        }
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages = {
            "does_not_exist":"Geçersiz bir kategori girdiniz",
            "incorrect_type":"Kategori Id sayısal olmalıdır."
        }
    )

    class Meta: 
        model = Product
        fields = ["name", "slug", "price","category", "description","stock","isHome","isActive"]

    def validate_name(self, value):
        return validations.validate_name(value)
    
    def validate_price(self, value):
        return validations.validate_price(value)
    
    def validate_slug(self, value):
        return validations.validate_slug(value)
    
    def validate(self, data):
        return validations.validate_product_object(data)

    
class ProductUpdateSerializer(serializers.ModelSerializer):

    isHome = serializers.BooleanField(required=False)
    isActive = serializers.BooleanField(required=False)

    stock = serializers.IntegerField(
        min_value=0,
        required=False,
        error_messages  = {
            "min_value": "Stok negatif değer olamaz."
        }
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages = {
            "does_not_exist":"Geçersiz bir kategori girdiniz",
            "incorrect_type":"Kategori Id sayısal olmalıdır."
        }
    )

    class Meta: 
        model = Product
        fields = ["name", "description", "slug", "stock", "price","category","isHome","isActive" ]

    def validate_name(self, value):
        return validations.validate_name(value)
    
    def validate_price(self, value):
        return validations.validate_price(value)
    
    def validate_slug(self, value):
        return validations.validate_slug(value, instance=self.instance)
    
    def validate(self, data):
        return validations.validate_product_object(data)

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        exclude = ["isHome","isActive"]
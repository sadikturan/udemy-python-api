from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price","category"]

class ProductCreateSerializer(serializers.ModelSerializer):

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
        fields = ["name", "slug", "price","category", "description","stock"]

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Ürün adı en az 3 karakter olmalıdır.")
        
        if len(value) > 200:
            raise serializers.ValidationError("Ürün adı en çok 200 karakter olmalıdır.")
        
        return value
    
    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError("Fiyat sıfırdan büyük olmalıdır.")
        return value
    
    def validate_slug(self, value):
        if Product.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Bu slug zaten kullanılıyor.")
        return value
    
class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ["name", "description", "slug", "stock", "price","category","isHome","isActive" ]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        exclude = ["isHome","isActive"]
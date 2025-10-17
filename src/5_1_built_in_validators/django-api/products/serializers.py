from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price","category"]

class ProductCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=3, max_length=200,error_messages= {
        "min_length": "Ürün adı en az 3 karakter olmalıdır.",
        "max_length": "Ürün adı en fazla 200 karakter olmalıdır.",
    })

    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value = 1,
        error_messages  = {
            "min_value": "Fiyat sıfırdan büyük olmalıdır."
        }
    )

    stock = serializers.IntegerField(
        min_value=0,
        error_messages  = {
            "min_value": "Stok negatif değer olamaz."
        }
    )

    slug = serializers.SlugField(
        validators = [UniqueValidator(queryset=Product.objects.all(), message="Bu slug zaten kullanılıyor.")]
    )

    class Meta: 
        model = Product
        fields = ["name", "slug", "price","category", "description","stock"]

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ["name", "description", "slug", "stock", "price","category","isHome","isActive" ]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        exclude = ["isHome","isActive"]
from rest_framework import serializers
from .models import Product
from categories.models import Category
from . import validations
from comments.serializers import CommentSerializer

class BaseProductSerializer(serializers.ModelSerializer):    

    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages = {
            "does_not_exist":"Geçersiz bir kategori girdiniz",
            "incorrect_type":"Kategori Id sayısal olmalıdır."
        }
    )

    class Meta: 
        model = Product

    def validate_name(self, value):
        return validations.validate_name(value)
    
    def validate_price(self, value):
        return validations.validate_price(value)
    
    def validate_slug(self, value):
        return validations.validate_slug(value, instance=self.instance)
    
    def validate(self, data):
        return validations.validate_product_object(data)

class ProductCreateSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        exclude = ["id","stock","isHome","isActive"]
    
class ProductUpdateSerializer(BaseProductSerializer):
    isHome = serializers.BooleanField(required=False)
    isActive = serializers.BooleanField(required=False)
    stock = serializers.IntegerField(
        min_value=0,
        required=False,
        error_messages  = {
            "min_value": "Stok negatif değer olamaz."
        }
    )

    class Meta(BaseProductSerializer.Meta):
        exclude = ["id"]
    

class ProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True) 
    class Meta: 
        model = Product
        exclude = ["isHome","isActive"]

class AdminProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True) 
    class Meta: 
        model = Product
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id","name", "slug", "price","category"]

class AdminProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id","name", "slug","stock","price","category","isActive","isHome"]

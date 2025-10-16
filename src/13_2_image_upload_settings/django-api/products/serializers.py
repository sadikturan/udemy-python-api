from rest_framework import serializers
from .models import Product, ProductImage
from .services import validate_uploaded_image
from categories.models import Category
from rest_framework.validators import UniqueValidator
from comments.serializers import CommentSerializer
from categories.serializers import CategorySerializer, CategoryListSerializer
import re

class OrderProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug']

class ProductImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image','alt_text']

    def validate_image(self, image):
        validate_uploaded_image(image)
        return image

class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    class Meta:
        model = Product
        fields = ['id','name','price','stock','slug','category']

class ProductDetailsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id','name','description','price','stock','slug','category','comments']

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, validators = [UniqueValidator(queryset=Product.objects.all())])
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages = {
            'does_not_exist': "The selected category is not available.",
            'incorrect_type': "The category id is invalid.",
        }
    )

    class Meta:
        model = Product
        fields = ['id','name','description','price','stock','slug','category']

    def validate_name(self,value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters.")
        return value
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be greater that 0.")
        
        if value > 100000:
            raise serializers.ValidationError("Price seems unusually high.")
        
        return value
        
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        
        return value
        
    def validate_slug(self, value):
        if self.instance is None:
            if Product.objects.filter(slug = value).exists():
                raise serializers.ValidationError("Slug must be unique.")
        else:
            if Product.objects.filter(slug=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Slug must be unique.")

        if not re.match('^[a-z0-9]+(?:-[a-z0-9]+)*$', value):
            raise serializers.ValidationError("Slug must be lowercase and can only contain hyphens and alphanumeric characters.")
        
        return value
        
    def validate(self, data):
        return data

 
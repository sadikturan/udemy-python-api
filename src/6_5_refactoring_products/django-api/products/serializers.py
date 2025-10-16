from rest_framework import serializers
from .models import Product
from categories.models import Category
from rest_framework.validators import UniqueValidator
from comments.serializers import CommentSerializer
from categories.serializers import CategorySerializer
import re

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
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
    comments = CommentSerializer(many=True, read_only=True)
    name = serializers.CharField(max_length=200, validators = [UniqueValidator(queryset=Product.objects.all())])
    slug = serializers.CharField(validators = [UniqueValidator(queryset=Product.objects.all())])

    class Meta:
        model = Product
        # fields = "__all__"
        fields = ['id','name','description','price','stock','slug','category','comments']

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
        if not re.match('^[a-z0-9]+(?:-[a-z0-9]+)*$', value):
            raise serializers.ValidationError("Slug must be lowercase and can only contain hyphens and alphanumeric characters.")
        
        return value
        
    def validate(self, data):
        return data

 
from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price',  max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id','product','product_name','product_price','quantity','total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    # user = serializers.StringRelatedField()
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','items','total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


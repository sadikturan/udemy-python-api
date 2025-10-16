from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

class CartItemUpdateSerializer(serializers.Serializer):
    quantity  = serializers.IntegerField(min_value=0)

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name","price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id","product","quantity","item_total"]

    def get_item_total(self, obj) -> float:
        return obj.get_item_total()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    cart_total = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Cart
        fields = ["id","user","items","cart_total"]

    def get_cart_total(self, obj) -> float:
        return obj.get_cart_total()


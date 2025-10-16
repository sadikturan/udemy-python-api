from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import OrderProductItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','user','created','updated','status','total_price','items']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
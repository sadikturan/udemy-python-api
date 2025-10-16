from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import OrderProductItemSerializer
from addresses.serializers import AddressDetailsSerializer
from payments.serializers import CardSerializer
from drf_spectacular.utils import extend_schema_field

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True, read_only=True)
    addresses = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id','user','created','updated','status','total_price','items','addresses']

    @extend_schema_field({
        "type": "object",
        "properties": {
            "delivery_address": {"type": "object"},
            "billing_address": {"type": "object"},
        }
    })
    def get_addresses(self, obj):
        return {
            'delivery_address': AddressDetailsSerializer(obj.delivery_address).data if obj.delivery_address else None,
            'billing_address': AddressDetailsSerializer(obj.billing_address).data if obj.billing_address else None,
        }

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderCreateRequestSerializer(serializers.Serializer):
    delivery_address_id = serializers.IntegerField()
    billing_address_id = serializers.IntegerField()
    card_data = CardSerializer()
    coupon_code = serializers.CharField(required=False, allow_blank=True)

class OrderCreateResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    order_id = serializers.IntegerField()
    payment = serializers.JSONField()
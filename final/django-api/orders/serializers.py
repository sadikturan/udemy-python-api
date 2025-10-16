from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from addresses.serializers import AddressSerializer
from payments.serializers import CardSerializer
from typing import List

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

class OrderCreateSerializer(serializers.Serializer):
    delivery_address_id =serializers.IntegerField()
    billing_address_id = serializers.IntegerField()
    card_data = CardSerializer()
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        delivery_address_id = data.get("delivery_address_id")
        billing_address_id = data.get("billing_address_id")

        if not delivery_address_id or not billing_address_id:
            raise serializers.ValidationError("Teslimatve fatura adresi girmelisiniz.")
        
        return data

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id","product","quantity","price"]
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True,read_only=True)
    addresses = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id","user","created","updated","status","order_total","items","addresses"]

    def get_addresses(self, obj) -> List[str]:
        return {
            'delivery_address': AddressSerializer(obj.delivery_address).data if obj.delivery_address else None,
            'billing_address': AddressSerializer(obj.billing_address).data if obj.billing_address else None,
        }

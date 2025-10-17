from rest_framework import serializers

class OrderCreateSerializer(serializers.Serializer):
    delivery_address_id =serializers.IntegerField()
    billing_address_id = serializers.IntegerField()

    def validate(self, data):
        delivery_address_id = data.get("delivery_address_id")
        billing_address_id = data.get("billing_address_id")

        if not delivery_address_id or not billing_address_id:
            raise serializers.ValidationError("Teslimatve fatura adresi girmelisiniz.")
        
        return data

from rest_framework import serializers

class CardSerializer(serializers.Serializer):
    card_name = serializers.CharField(max_length=50)
    card_number = serializers.CharField(max_length=16)
    expiry_month = serializers.IntegerField(min_value=1, max_value=12)
    expiry_year = serializers.IntegerField(min_value=2025)
    cvc = serializers.CharField(max_length=3)
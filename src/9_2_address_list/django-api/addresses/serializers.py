from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Address
        fields = "__all__"
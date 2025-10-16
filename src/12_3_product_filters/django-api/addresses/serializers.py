from rest_framework import serializers
from .models import Address, City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']

class AddressListSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = ['id','full_name','district','city', 'address_type','is_default','user']

class AddressDetailsSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = ['id','full_name','phone','address_line','district','city', 'street','postal_code','address_type','is_default']

class AddressSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source="city")

    class Meta:
        model = Address
        fields = ['full_name','phone','address_line','district','city_id', 'street','postal_code','address_type','is_default']
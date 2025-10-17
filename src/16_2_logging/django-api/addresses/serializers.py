from rest_framework import serializers
from .models import Address, City

class AddressSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = ["id","full_name","district","city","address_type"]

class AddressDetailSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = "__all__"

class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Address
        exclude = ["user","created"]
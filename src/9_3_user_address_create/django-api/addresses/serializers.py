from rest_framework import serializers
from .models import Address, City

class AddressSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = "__all__"

class AddressCreateSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Address
        exclude = ["user","created"]
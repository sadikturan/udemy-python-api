from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
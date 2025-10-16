from rest_framework import serializers
from .models import Category
from rest_framework.validators import UniqueValidator

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=Category.objects.all())])
    description = serializers.CharField(required=False,allow_blank=True,allow_null=True)

    def validate(self, data):
        name = data.get("name")
        description = data.get("description")

        if description and name == description:
            raise serializers.ValidationError("Name and Description should be different.")
        
        return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("You must enter at least 2 charactes")
        
        # if Category.objects.filter(name=value).exists():
        #     raise serializers.ValidationError("This category name is already in use.")

        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
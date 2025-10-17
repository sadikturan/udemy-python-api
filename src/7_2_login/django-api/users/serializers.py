from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username ve şifre gereklidir.")
        
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Geçersiz username veya şifre.")
        
        attrs["user"] = user

        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "password_confirm"]

    def validate(self,  attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm":"Şifreler eşleşmiyor"})
        
        user = User(
            username = attrs.get("username"),
            email = attrs.get("email"),
            first_name = attrs.get("first_name"),
            last_name = attrs.get("last_name"),
        )
        
        validate_password(attrs["password"], user=user)
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


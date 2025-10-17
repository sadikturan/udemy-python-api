from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.username if obj.user else None
    
    def get_active(self, obj):
        return obj.is_valid()
    
class UserCouponSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ["usage_limit","usage_count"]

    def get_user(self, obj):
        return obj.user.username if obj.user else None
    
    def get_active(self, obj):
        return obj.is_valid()
    
    


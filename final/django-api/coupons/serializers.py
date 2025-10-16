from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = "__all__"

    def get_user(self, obj) -> str:
        return obj.user.username if obj.user else None
    
    def get_active(self, obj) -> bool:
        return obj.is_valid()
    
class CouponCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = "__all__"
    
    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Kupon kodu boş olamaz.")
        return value
    
    def validate_discount_percent(self, value):
        if value is not None and (value < 0 or value >100):
            raise serializers.ValidationError("İndirim yüzdesi 0 ile 100 arasında olmaldır.")
        return value
    
    def validate_discount_amount(self, value):
        if value is not None and  value < 0:
            raise serializers.ValidationError("İndirim tutarı negatif olamaz.")
        return value
        
    def validate_usage_limit(self, value):
        if value is not None and  value < 0:
            raise serializers.ValidationError("Kullanım limiti negatif olamaz.")
        return value
        
    def validate(self, data):
        discount_percent = data.get("discount_percent", getattr(self.instance, "discount_percent", None))
        discount_amount = data.get("discount_amount", getattr(self.instance, "discount_amount", None))

        if (discount_percent is None) and (discount_amount is None):
            raise serializers.ValidationError("En az bir indirim türü belirtmelisiniz.")

        start_data = data.get("start_date")    
        end_date = data.get("end_date")    

        if start_data and end_date and start_data >= end_date:
            raise serializers.ValidationError("Başlangıç tarihi bitiş tarihinden önce olmalıdır.")
        
        return data
    
    
    
class UserCouponSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ["usage_limit","usage_count"]

    def get_user(self, obj) -> str:
        return obj.user.username if obj.user else None
    
    def get_active(self, obj) -> bool:
        return obj.is_valid()
    
    


from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id',
            'code',
            'discount_percent',
            'discount_amount',
            'start_date',
            'end_date',
            'active',
            'usage_limit',
            'usage_count',
        ]
        read_only_fields = ['usage_count']
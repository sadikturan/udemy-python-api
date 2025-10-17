from rest_framework import generics, permissions
from .models import Coupon
from . import serializers

class AdminCouponList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Coupon.objects.all()
    serializer_class = serializers.CouponSerializer

class UserCouponList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = serializers.UserCouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(user=self.request.user)

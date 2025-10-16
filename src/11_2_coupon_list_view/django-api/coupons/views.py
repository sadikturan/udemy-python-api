from django.shortcuts import render
from rest_framework.views import APIView
from .models import Coupon
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import CouponSerializer
from django.shortcuts import get_object_or_404

class AdminCouponList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)
    
class AdminCouponDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

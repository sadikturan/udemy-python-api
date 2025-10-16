from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Coupon
from .serializers import CouponSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Kuponları Listele (Admin)",
        description="Tüm kuponları listeler. Sadece admin erişimine açıktır.",
        tags=["Coupons"],
        responses=CouponSerializer(many=True)
    ),
    post=extend_schema(
        summary="Kupon Oluştur (Admin)",
        description="Yeni bir kupon oluşturur. Sadece admin erişimine açıktır.",
        tags=["Coupons"],
        request=CouponSerializer,
        responses={201: CouponSerializer}
    )
)
class AdminCouponListCreateView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
    
@extend_schema_view(
    get=extend_schema(
        summary="Kupon Detayı (Admin)",
        description="Belirli bir kuponun detaylarını döner. (Sadece admin erişimi)",
        tags=["Coupons"],
        responses=CouponSerializer
    ),
    put=extend_schema(
        summary="Kuponu Güncelle (PUT) (Admin)",
        description="Belirli bir kuponun tüm alanlarını günceller. (Sadece admin erişimi)",
        request=CouponSerializer,
        responses=CouponSerializer,
        tags=["Coupons"]
    ),
    patch=extend_schema(
        summary="Kuponu Güncelle (PATCH) (Admin)",
        description="Belirli bir kuponun bazı alanlarını günceller. (Sadece admin erişimi)",
        request=CouponSerializer,
        responses=CouponSerializer,
        tags=["Coupons"]
    ),
    delete=extend_schema(
        summary="Kupon Sil (Admin)",
        description="Belirli bir kuponu siler. (Sadece admin erişimi)",
        tags=["Coupons"]
    )
)
class AdminCouponRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
    


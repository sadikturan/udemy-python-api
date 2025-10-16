from rest_framework import generics, permissions
from .models import Coupon
from . import serializers
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    get=extend_schema(
        summary="Kuponları Listele (Admin)",
        description="Tüm kuponları listeler. Sadece admin erişebilir.",
        responses=serializers.CouponSerializer(many=True),
        tags=["Coupon"],
    ),
    post=extend_schema(
        summary="Yeni Kupon Oluştur (Admin)",
        description="Admin tarafından yeni bir kupon oluşturulur.",
        request=serializers.CouponCreateUpdateSerializer,
        responses=serializers.CouponSerializer,
        tags=["Coupon"],
    ),
)
class AdminCouponCreateList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Coupon.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CouponCreateUpdateSerializer
        return serializers.CouponSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Kupon Detayı (Admin)",
        description="Belirtilen ID'ye sahip kuponun detaylarını döner. Sadece admin erişebilir.",
        responses=serializers.CouponSerializer,
        tags=["Coupon"],
    ),
    put=extend_schema(
        summary="Kupon Güncelle (PUT, Admin)",
        description="Kuponun tüm alanlarını günceller (tam güncelleme).",
        request=serializers.CouponCreateUpdateSerializer,
        responses=serializers.CouponSerializer,
        tags=["Coupon"],
    ),
    patch=extend_schema(
        summary="Kupon Güncelle (PATCH, Admin)",
        description="Kuponun bazı alanlarını günceller (kısmi güncelleme).",
        request=serializers.CouponCreateUpdateSerializer,
        responses=serializers.CouponSerializer,
        tags=["Coupon"],
    ),
    delete=extend_schema(
        summary="Kupon Sil (Admin)",
        description="Belirtilen kuponu siler. Bu işlem sadece admin tarafından yapılabilir.",
        responses={204: {"message": "Coupon deleted"}},
        tags=["Coupon"],
    ),
)
class AdminCouponDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Coupon.objects.all()
    lookup_url_kwarg = "coupon_id"

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CouponCreateUpdateSerializer
        return serializers.CouponSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Kullanıcı Kuponlarını Listele",
        description="Giriş yapmış kullanıcının sahip olduğu kuponları listeler.",
        responses=serializers.UserCouponSerializer(many=True),
        tags=["Coupon"],
    )
)
class UserCouponList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = serializers.UserCouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(user=self.request.user)

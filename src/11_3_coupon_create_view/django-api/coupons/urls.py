from django.urls import path
from .views import AdminCouponList, AdminCouponDetail, AdminCouponCreate

urlpatterns = [
    path('admin/', AdminCouponList.as_view(), name="admin_coupon_list"),
    path('admin/<int:pk>', AdminCouponDetail.as_view(), name="admin_coupon_detail"),
    path('admin/create', AdminCouponCreate.as_view(), name="admin_coupon_create"),



]

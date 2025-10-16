from django.urls import path
from .views import  AdminCouponRetrieveUpdateDestroyView, AdminCouponListCreateView

urlpatterns = [
    path('admin/', AdminCouponListCreateView.as_view(), name="admin_coupon_list_create"),
    path('admin/<int:pk>', AdminCouponRetrieveUpdateDestroyView.as_view(), name="admin_coupon_detail"),
]

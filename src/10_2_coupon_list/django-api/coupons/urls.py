from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCouponList.as_view(), name='coupon_list'),
    path('admin', views.AdminCouponList.as_view(), name='admin_coupon_list'),
]

from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent','discount_amount','start_date','end_date','active','usage_limit','usage_count',)
    list_filter = ('active','start_date','end_date',)
    search_fields = ('code',)
    readonly_fields = ('usage_count',)
    ordering = ('-end_date',)

from .models import Coupon
from rest_framework.exceptions import ValidationError
from decimal import Decimal

def get_valid_coupon_or_none(code):
    if not code:
        return None
    
    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        raise ValidationError("Kupon bulunamadı.")
    
    if not coupon.is_valid():
        raise ValidationError("Kupon geçerli değil.")
    
    return coupon

def apply_coupon_discount(order, coupon):
    if coupon.discount_percent:
        discount = order.order_total * (Decimal(coupon.discount_percent) / Decimal(100))
    elif coupon.discount_amount:
        discount = Decimal(coupon.discount_amount)
    else:
        discount =  Decimal(0)

    order.order_total -= discount
    order.order_total = max(order.order_total, 0)
    order.save()

    return discount

def increment_coupon_usage(coupon):
    coupon.usage_count += 1
    coupon.save()


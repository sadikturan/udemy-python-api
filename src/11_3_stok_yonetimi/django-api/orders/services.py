from rest_framework.exceptions import ValidationError
from  .models import Order, OrderItem
from products.services import check_product_stock, decrease_product_stock
from django.db import transaction

@transaction.atomic
def create_order_from_cart(user, cart, delivery_address_id, billing_address_id):
    cart_items = cart.items.select_related("product").all()

    if not cart_items:
        raise ValidationError({'error': 'Your cart is empty.'})
    
    order = Order.objects.create(
        user=user, 
        delivery_address_id=delivery_address_id, 
        billing_address_id=billing_address_id
    )

    for item in cart_items:
        check_product_stock(item.product, item.quantity)

        OrderItem.objects.create(
            order = order,
            product = item.product,
            quantity = item.quantity
        )

        decrease_product_stock(item.product, item.quantity)

    order.calculate_total()

    cart.items.all().delete()

    return order
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from products.services import check_product_stock, decrease_product_stock
from django.db import transaction
from addresses.services import get_user_address_or_404
from payments import create_payment

@transaction.atomic
def create_order_from_cart(user, cart, delivery_address_id, billing_address_id, card_data):
    cart_items = cart.items.select_related("product").all()

    if not cart_items:
        raise ValidationError({'error': 'Your cart is empty.'})
    
    delivery_address = get_user_address_or_404(user, delivery_address_id)
    billing_address = get_user_address_or_404(user, billing_address_id)
        
    order = Order.objects.create(
        user=user, 
        delivery_address=delivery_address, 
        billing_address=billing_address
    )

    for item in cart_items:
        check_product_stock(item.product, item.quantity)

        OrderItem.objects.create(
            order = order,
            product = item.product,
            quantity = item.quantity,
            price = item.product.price
        )

    order.calculate_total()

    payment_result = create_payment(user, order, card_data)

    cart.items.all().delete()

    return order, payment_result
      
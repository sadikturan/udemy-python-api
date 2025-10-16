from .models import Cart, CartItem
from products.services import get_product_or_404, check_product_stock
from rest_framework.exceptions import NotFound

def get_cart_or_create(user):
    cart, created = Cart.objects.get_or_create(user = user) 
    return cart

def get_cart_item_or_404(cart_item_id, user):
    try:
        return CartItem.objects.get(pk=cart_item_id, cart__user = user)
    except CartItem.DoesNotExist:
        raise NotFound({'error': 'Cart item not found.'})

def add_product_to_cart(user, product_id, quantity):
    cart = get_cart_or_create(user)
    product = get_product_or_404(product_id)
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)

    if created:
        check_product_stock(product, quantity)
        cart_item.quantity = quantity
    else:
        new_quantity = cart_item.quantity + quantity
        check_product_stock(product, new_quantity)
        cart_item.quantity = new_quantity

    cart_item.save()

def update_cart_item_quantity(cart_item, quantity):
    if int(quantity) <= 0:
        cart_item.delete()
        return None
    
    check_product_stock(cart_item.product, quantity)

    cart_item.quantity = quantity
    cart_item.save()
    return cart_item
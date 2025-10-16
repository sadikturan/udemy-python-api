from .models import Cart, CartItem
from products.services import get_product_or_404, check_product_stock

def get_cart_or_create(user):
    cart, created = Cart.objects.get_or_create(user = user) 
    return cart

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
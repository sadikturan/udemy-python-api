from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from rest_framework.response import Response

def check_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError(f"Stokta sadece {product.stock} adet mevcut.")
    
def add_product_to_cart(user, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    check_product_stock(product, quantity)

    cart, _ = Cart.objects.get_or_create(user = user)
    cart_item, itemCreated = CartItem.objects.get_or_create(cart=cart,product=product)

    if not itemCreated:
        new_quantity = cart_item.quantity + quantity
        check_product_stock(product, new_quantity)
        cart_item.quantity = new_quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return cart

def update_cart_item(user, cart_item_id, quantity):
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id, cart__user = user)
    except CartItem.DoesNotExist:
        raise ValidationError("Cart item not found")
    
    if quantity <= 0:
        cart_item.delete()
    else:
        check_product_stock(cart_item.product, quantity)
        cart_item.quantity = quantity
        cart_item.save()

    return cart_item.cart    

def delete_cart_item(user, cart_item_id):
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id, cart__user=user)
    except CartItem.DoesNotExist:
        raise ValidationError("Cart item not found")
    
    cart_item.delete()

    return cart_item.cart    

def clear_cart(user):
    cart, _ = Cart.objects.get_or_create(user = user)
    cart.items.all().delete()
    return cart
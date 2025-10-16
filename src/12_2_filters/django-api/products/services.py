from .models import Product
from rest_framework.exceptions import NotFound, ValidationError

def get_product_or_404(product_id):
    try:
        return Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise NotFound('Product not found')
    
def check_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError(f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {quantity}")
    
def decrease_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError(f"Cannot decrease stock by {quantity}. Only {product.stock} items available.")
    
    product.stock -= quantity
    product.save()
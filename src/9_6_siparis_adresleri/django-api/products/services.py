from .models import Product
from rest_framework.exceptions import NotFound, ValidationError

def get_product_or_404(category_id):
    try:
        return Product.objects.get(pk=category_id)
    except Product.DoesNotExist:
        raise NotFound({'error': 'Product not found'})
    
def check_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError({'error': f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {quantity}"})
    
def decrease_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError({'error': f"Cannot decrease stock by {quantity}. Only {product.stock} items available."})
    
    product.stock -= quantity
    product.save()
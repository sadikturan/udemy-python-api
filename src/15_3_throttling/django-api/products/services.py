from rest_framework.exceptions import ValidationError, NotFound
from .models import Product

def check_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError(f"Stokta sadece {product.stock} adet mevcut.")
    
def decrease_product_stock(product, quantity):
    product.stock -= quantity
    product.save()

def get_product_or_404(product_id):
    try:
        return Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise NotFound("Product not found")
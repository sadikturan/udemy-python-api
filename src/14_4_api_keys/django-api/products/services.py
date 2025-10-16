from .models import Product
from rest_framework.exceptions import NotFound, ValidationError
import os

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

ALLOWED_EXTENSIONS = ['.jpg', '.jpeg']
MAX_FILE_SIZE_MB = 3

def validate_uploaded_image(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Unsupported file extension: {ext}. Only .jpg and .jpeg are allowed.')
    
    file_size_mb = file.size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValidationError(f'File size exceeds limit. Max allowed is {MAX_FILE_SIZE_MB} MB.')
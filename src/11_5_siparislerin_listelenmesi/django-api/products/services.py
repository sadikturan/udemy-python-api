from rest_framework.exceptions import ValidationError

def check_product_stock(product, quantity):
    if quantity > product.stock:
        raise ValidationError(f"Stokta sadece {product.stock} adet mevcut.")
    
def decrease_product_stock(product, quantity):
    product.stock -= quantity
    product.save()

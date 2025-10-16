from django.contrib import admin
from .models import Product, ProductImage

admin.site.register(Product)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'alt_text', 'image']
    list_filter = ['product']
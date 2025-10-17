from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'isHome', 'isActive', 'category')
    list_filter = ('isHome', 'isActive', 'category')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name','description',)
    ordering = ('name',)

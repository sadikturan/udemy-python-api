from django.contrib import admin
from .models import Address, City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','address_line','city','is_default']
    list_filter = ['city']
    search_fields = ['full_name','address_line','city','postal_code']

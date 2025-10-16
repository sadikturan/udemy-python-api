import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact','iexact','contains','icontains'],
            'price': ['exact', 'lt', 'gt', 'range'],
            'category': ['exact']
        }

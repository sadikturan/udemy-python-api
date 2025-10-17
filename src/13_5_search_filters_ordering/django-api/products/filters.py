import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    class Meta:
        model = Product
        fields = {
            "name": ["iexact","icontains"],
            "price": ["exact","lt","gt","range"],
            "isHome": ["exact"],
            "category": ["exact"]
        }
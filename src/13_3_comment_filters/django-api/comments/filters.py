import django_filters
from .models import Comment

class CommentFilter(django_filters.FilterSet):
    # created_after = django_filters.DateFilter(field_name="created", lookup_expr="gte")
    # created_before = django_filters.DateFilter(field_name="created", lookup_expr="lte")

    # rating = django_filters.NumberFilter(field_name="rating", lookup_expr="exact")
    # min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    # max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="lte")

    class Meta:
        model = Comment
        fields = {
            'product': ['exact'],
            'user': ['exact'],
            'rating': ['exact', 'gte', 'lte'],  # rating__exact=5, rating__gte=4
            'created': ['exact', 'gte', 'lte'],
        }
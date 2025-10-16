import django_filters
from .models import Comment

class CommentFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(field_name="created", lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name="created", lookup_expr='lte')

    class Meta:
        model = Comment
        fields = ['product','user','active','rating','created']
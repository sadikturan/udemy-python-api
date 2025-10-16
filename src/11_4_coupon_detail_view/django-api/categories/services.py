from .models import Category
from rest_framework.exceptions import NotFound

def get_category_or_404(category_id):
    try:
        return Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise NotFound({'error': 'Category not found'})
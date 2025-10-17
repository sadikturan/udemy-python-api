from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

class Comment(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return str(self.rating) + " | " + self.product.name

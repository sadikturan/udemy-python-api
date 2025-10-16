from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
from users.models import CustomUser

class Comment(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, models.CASCADE)

    def __str__(self):
        return str(self.rating) + " | " + self.product.name

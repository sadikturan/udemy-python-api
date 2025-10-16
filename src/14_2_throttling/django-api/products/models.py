from django.db import models
from categories.models import Category

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name
    
def product_image_upload_to(instance, filename):
    return f"products/{instance.product.id}/{filename}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_image_upload_to)
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.id}"
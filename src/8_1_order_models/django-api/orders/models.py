from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices= [
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
    
    def calculate_total(self):
        total = sum([item.product.price * item.quantity for item in self.items.all()])
        self.total_price = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.price = self.product.price
        super().save(*args, **kwargs)


    

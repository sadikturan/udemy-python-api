from django.db import models
from django.contrib.auth.models import User
from addresses.models import Address
from coupons.models import Coupon
from products.models import Product
from .constants import ORDER_STATUS_CHOICES

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="orders")
    delivery_address = models.ForeignKey(Address, on_delete=models.RESTRICT, related_name="delivery_addresses")
    billing_address = models.ForeignKey(Address, on_delete=models.RESTRICT, related_name="billing_addresses")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending',  error_messages={
        'invalid_choice': 'Invalid status. Valid options are: pending, processing, shipped, completed, canceled'
    })

    def __str__(self):
        return f"Order #{self.id} by{self.user}"
    
    def calculate_total(self):
        total = sum([(item.price * item.quantity) for item in self.items.all()])    
        self.order_total = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.price and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


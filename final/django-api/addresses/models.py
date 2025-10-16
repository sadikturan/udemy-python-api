from django.db import models
from  django.contrib.auth.models import User

ADDRESS_TYPES = {
    ('home', 'Home'),
    ('work', 'Work'),
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
}

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='home')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.address_line}, {self.city}"


from django.db import models
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

ADDRESS_TYPES = (
    ('home', 'Home'),
    ('work', 'Work'),
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, related_name="addresses", on_delete=models.PROTECT)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='home')
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.address_line}, {self.city}"
    
    class Meta:
        ordering = ['-created']

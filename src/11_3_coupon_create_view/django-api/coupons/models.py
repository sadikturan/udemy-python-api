from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    usage_count =  models.PositiveIntegerField(default=0)

    def is_valid(self):
        now = timezone.now()

        return (
            self.active
            and self.start_date <= now <= self.end_date
            and (self.usage_limit is None or self.usege_count < self.usage_limit)
        )
    
    def __str__(self):
        return self.code


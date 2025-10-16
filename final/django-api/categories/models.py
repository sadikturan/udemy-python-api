from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    icon = models.CharField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

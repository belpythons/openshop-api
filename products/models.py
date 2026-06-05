import uuid
from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    shop = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    picture = models.CharField(max_length=500, blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

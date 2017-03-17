from __future__ import unicode_literals

from django.db import models

class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True, editable=False)

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Item(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True, editable=False)

    product = models.ForeignKey(Product)
    order = models.ForeignKey('Order', related_name='items')
    quantity = models.IntegerField()

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True, editable=False)

    def total(self):
        return sum(i.quantity * i.product.price for i in self.items.all())

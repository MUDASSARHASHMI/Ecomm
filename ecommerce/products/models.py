from __future__ import unicode_literals

from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title
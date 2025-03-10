from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    critical_quantity = models.PositiveIntegerField(default=0)

    def is_critical(self):
        return self.quantity < self.critical_quantity

    def __str__(self):
        return self.name



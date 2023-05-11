from core.models import AuditableModel
from django.db import models


class Product(AuditableModel):
    name = models.DecimalField(max_digits=8, decimal_places=2)
    description =  models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
from core.models import AuditableModel
from django.db import models


class Product(AuditableModel):
    name = models.CharField(max_length=50)
    description =  models.TextField(blank=True, null=True)
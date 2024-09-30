from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    description = models.TextField(blank=True, null=True) 
    quantity = models.PositiveIntegerField(default=0)  
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name

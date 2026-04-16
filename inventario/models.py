from django.db import models

# Create your models here.
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

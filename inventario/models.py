from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    # Este campo se encarga de conectar con Azure Blob Storage para almacenar la imagen
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
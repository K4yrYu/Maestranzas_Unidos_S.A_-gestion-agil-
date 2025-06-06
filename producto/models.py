from django.db import models
from proveedores.models import Proveedor  # NUEVO


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre  
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    numero_de_serie = models.PositiveIntegerField(default=0) # actuara como num serie
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    stock_minimo = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    imagen = models.URLField(max_length=300, blank=True, null=True)
    activo = models.BooleanField(default=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)  # NUEVO

    def __str__(self):
        return self.nombre

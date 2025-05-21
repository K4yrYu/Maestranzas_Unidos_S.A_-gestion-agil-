from django.db import models
from django.contrib.auth.models import User
from producto.models import Producto
from proveedores.models import Proveedor  # ✅ Importación correcta del proveedor

class OrdenCompra(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('recibida', 'Recibida'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor.nombre}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} (Orden #{self.orden.id})"

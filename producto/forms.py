
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'stock', 'stock_minimo',
            'categoria', 'lote', 'fecha_vencimiento', 'imagen', 'activo',
            'proveedor'  # NUEVO
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),  # NUEVO
        }

from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    motivo = forms.CharField(
        label="Motivo del agregado",
        required=True,
        max_length=255
    )

    class Meta:
        model = Producto
        fields = [
            'nombre', 'numero_de_serie', 'precio', 'stock', 'stock_minimo',
            'categoria', 'lote', 'fecha_vencimiento', 'imagen', 'activo',
            'proveedor'
        ]
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['fecha_vencimiento', 'activo']:
                field.required = True
            else:
                field.required = False

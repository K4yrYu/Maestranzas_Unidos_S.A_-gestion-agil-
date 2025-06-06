from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rut', 'email', 'telefono', 'direccion', 'activo']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Todos los campos menos 'activo' serán obligatorios
        for name, field in self.fields.items():
            if name != 'activo':
                field.required = True
            else:
                field.required = False

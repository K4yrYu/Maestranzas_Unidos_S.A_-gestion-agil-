from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rut', 'email', 'telefono', 'direccion', 'activo']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

from django import forms
from .models import OrdenCompra

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from proveedores.models import Proveedor
        self.fields['proveedor'].queryset = Proveedor.objects.filter(activo=True)
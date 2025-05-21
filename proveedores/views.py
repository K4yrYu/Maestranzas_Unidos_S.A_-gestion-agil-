from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm
from django.contrib import messages

def lista_proveedores(request):
    proveedores_activos = Proveedor.objects.filter(activo=True)
    proveedores_inactivos = Proveedor.objects.filter(activo=False)
    return render(request, 'proveedores/lista_proveedores.html', {
        'proveedores_activos': proveedores_activos,
        'proveedores_inactivos': proveedores_inactivos,
    })

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado correctamente.")
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/formulario_proveedor.html', {
        'form': form,
        'modo': 'crear'
    })

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/formulario_proveedor.html', {
        'form': form,
        'modo': 'editar'
    })

def desactivar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    proveedor.activo = False
    proveedor.save()
    messages.warning(request, f"Proveedor '{proveedor.nombre}' desactivado.")
    return redirect('lista_proveedores')

def reactivar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.activo = True
    proveedor.save()
    return redirect('lista_proveedores')
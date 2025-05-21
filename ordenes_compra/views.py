from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from producto.models import Producto
from proveedores.models import Proveedor
from .models import OrdenCompra, ItemOrden
from .forms import OrdenCompraForm

@login_required
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all().order_by('-fecha_creacion')
    return render(request, 'ordenes_compra/lista_ordenes.html', {'ordenes': ordenes})

@login_required
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario = request.user
            orden.save()

            productos = request.POST.getlist('producto[]')
            cantidades = request.POST.getlist('cantidad[]')

            for prod_id, cant in zip(productos, cantidades):
                if prod_id and cant:
                    try:
                        producto = Producto.objects.get(pk=prod_id)
                        if producto.proveedor == orden.proveedor:
                            cantidad = int(cant)
                            if cantidad > 0:
                                ItemOrden.objects.create(
                                    orden=orden,
                                    producto=producto,
                                    cantidad=cantidad
                                )
                    except (Producto.DoesNotExist, ValueError):
                        continue

            return redirect('lista_ordenes')
    else:
        form = OrdenCompraForm()

    productos = Producto.objects.all()
    return render(request, 'ordenes_compra/formulario_orden.html', {
        'form': form,
        'productos': productos
    })

@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    items = orden.items.all()
    return render(request, 'ordenes_compra/detalle_orden.html', {
        'orden': orden,
        'items': items
    })

@login_required
def cambiar_estado(request, orden_id, nuevo_estado):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    orden.estado = nuevo_estado
    orden.save()
    return redirect('lista_ordenes')

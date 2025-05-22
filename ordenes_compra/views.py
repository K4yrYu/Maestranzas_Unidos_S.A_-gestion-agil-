from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from producto.models import Producto
from proveedores.models import Proveedor
from .models import OrdenCompra, ItemOrden
from .forms import OrdenCompraForm
from movimientos.models import Movimiento  
from django.db.models import F


@login_required
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all().order_by('-fecha_creacion')
    return render(request, 'ordenes_compra/lista_ordenes.html', {'ordenes': ordenes})

@login_required
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')

        hay_productos_validos = any(prod and cant and int(cant) > 0 for prod, cant in zip(productos, cantidades))

        if form.is_valid() and hay_productos_validos:
            orden = form.save(commit=False)
            orden.usuario = request.user
            orden.save()

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
            if not hay_productos_validos:
                messages.error(request, "Debe seleccionar al menos un producto válido y una cantidad mayor a cero.")
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

    if nuevo_estado == 'recibida' and orden.estado != 'recibida':
        # 1. Actualizar estado
        orden.estado = 'recibida'
        orden.save()

        # 2. Actualizar stock y registrar movimientos
        for item in orden.items.all():
            producto = item.producto
            producto.stock += item.cantidad
            producto.activo = True  # por si estaba desactivado por stock = 0
            producto.save()

            Movimiento.objects.create(
                producto=producto,
                tipo='entrada',
                cantidad=item.cantidad,
                usuario=request.user
            )

        messages.success(request, f"Orden #{orden.id} marcada como recibida. Stock actualizado.")
    else:
        orden.estado = nuevo_estado
        orden.save()
        messages.info(request, f"Orden #{orden.id} marcada como '{orden.get_estado_display()}'.")

    return redirect('lista_ordenes')

@login_required
def crear_orden_desde_criticos(request):
    if request.method == 'POST':
        productos = Producto.objects.filter(stock__lte=F('stock_minimo'), activo=True)

        proveedores = productos.values_list('proveedor', flat=True).distinct()

        for prov_id in proveedores:
            prov_productos = productos.filter(proveedor__id=prov_id)
            orden = OrdenCompra.objects.create(proveedor_id=prov_id, usuario=request.user)

            for p in prov_productos:
                cantidad_sugerida = max(p.stock_minimo * 2 - p.stock, 1)
                ItemOrden.objects.create(
                    orden=orden,
                    producto=p,
                    cantidad=cantidad_sugerida
                )

        messages.success(request, "Órdenes generadas automáticamente desde productos críticos.")
        return redirect('lista_ordenes')
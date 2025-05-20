from django.shortcuts import render, redirect
from .models import Movimiento
from .forms import MovimientoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from producto.models import Producto

@login_required
def lista_movimientos(request):
    productos = Producto.objects.all()
    producto_id = request.GET.get('producto')  # id del producto seleccionado

    if producto_id:
        movimientos = Movimiento.objects.filter(producto_id=producto_id).select_related('producto', 'usuario').order_by('-fecha')
    else:
        movimientos = Movimiento.objects.select_related('producto', 'usuario').order_by('-fecha')

    return render(request, 'movimientos/lista_movimientos.html', {
        'movimientos': movimientos,
        'productos': productos,
        'producto_id': producto_id,
    })

@login_required
def nuevo_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            producto = movimiento.producto
            cantidad = movimiento.cantidad

            if movimiento.tipo == 'entrada':
                producto.stock += cantidad

            elif movimiento.tipo == 'salida':
                if not producto.activo:
                    messages.error(request, 'Este producto está inactivo y no puede registrar salidas.')
                    return render(request, 'movimientos/nuevo_movimiento.html', {'form': form})

                if producto.stock < cantidad:
                    messages.error(request, f'El stock disponible ({producto.stock}) es menor a lo solicitado.')
                    return render(request, 'movimientos/nuevo_movimiento.html', {'form': form})

                producto.stock -= cantidad

                # Desactiva producto si queda en cero
                if producto.stock == 0:
                    producto.activo = False

            producto.save()
            movimiento.save()
            messages.success(request, 'Movimiento registrado correctamente.')
            return redirect('lista_movimientos')
    else:
        # Limita el queryset a solo productos activos para evitar salidas de inactivos
        form = MovimientoForm()
        form.fields['producto'].queryset = Producto.objects.filter(activo=True)

    return render(request, 'movimientos/nuevo_movimiento.html', {'form': form})

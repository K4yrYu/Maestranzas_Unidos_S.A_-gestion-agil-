from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from .forms import ProductoForm
from django.contrib import messages
from django.db.models import F
from datetime import datetime
from movimientos.models import Movimiento
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime


def lista_productos(request):
    productos = Producto.objects.all()
    categoria_seleccionada = request.GET.get("categoria")
    busqueda = request.GET.get("busqueda")

    if categoria_seleccionada:
        productos = productos.filter(categoria__id=categoria_seleccionada)

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    productos_activos = productos.filter(activo=True)
    productos_inactivos = productos.filter(activo=False)

    categorias = Producto.objects.values("categoria__id", "categoria__nombre").distinct()

    context = {
        "productos_activos": productos_activos,
        "productos_inactivos": productos_inactivos,
        "categorias": [c for c in categorias if c["categoria__id"] is not None],
        "categoria_seleccionada": categoria_seleccionada or "",
    }
    return render(request, "producto/lista.html", context)


def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado correctamente.")
            return redirect("lista_productos")
    else:
        form = ProductoForm()
    return render(request, "producto/formulario.html", {"form": form, "titulo": "Agregar Producto"})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("lista_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "producto/formulario.html", {"form": form, "titulo": "Editar Producto"})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.activo = False
    producto.save()
    messages.warning(request, f"Producto '{producto.nombre}' fue desactivado.")
    return redirect("lista_productos")


def dashboard(request):
    total_productos = Producto.objects.count()
    productos_activos = Producto.objects.filter(activo=True).count()
    productos_inactivos = Producto.objects.filter(activo=False).count()
    productos_stock_bajo = Producto.objects.filter(activo=True, stock__lte=F("stock_minimo")).count()
    total_categorias = Categoria.objects.count()

    now = datetime.now()
    entradas_mes = Movimiento.objects.filter(tipo='entrada', fecha__month=now.month).count()
    salidas_mes = Movimiento.objects.filter(tipo='salida', fecha__month=now.month).count()

    context = {
        "productos_total": total_productos,
        "productos_activos": productos_activos,
        "productos_inactivos": productos_inactivos,
        "productos_stock_bajo": productos_stock_bajo,
        "categorias": total_categorias,
        "entradas_mes": entradas_mes,
        "salidas_mes": salidas_mes,
    }

    return render(request, "producto/dashboard.html", context)

#####3

def exportar_excel_resumen(request):
    now = datetime.now()

    entradas = Movimiento.objects.filter(tipo='entrada', fecha__month=now.month)
    salidas = Movimiento.objects.filter(tipo='salida', fecha__month=now.month)
    stock_bajo = Producto.objects.filter(activo=True, stock__lte=F("stock_minimo"))
    inventario = Producto.objects.all()

    df_entradas = pd.DataFrame.from_records(entradas.values('fecha', 'producto__nombre', 'tipo', 'cantidad', 'usuario__username')).rename(columns={
        'fecha': 'Fecha',
        'producto__nombre': 'Producto',
        'tipo': 'Tipo',
        'cantidad': 'Cantidad',
        'usuario__username': 'Usuario'
    })
    df_salidas = pd.DataFrame.from_records(salidas.values('fecha', 'producto__nombre', 'tipo', 'cantidad', 'usuario__username')).rename(columns={
        'fecha': 'Fecha',
        'producto__nombre': 'Producto',
        'tipo': 'Tipo',
        'cantidad': 'Cantidad',
        'usuario__username': 'Usuario'
    })
    df_stock_bajo = pd.DataFrame.from_records(stock_bajo.values('nombre', 'stock', 'stock_minimo')).rename(columns={
        'nombre': 'Producto',
        'stock': 'Stock actual',
        'stock_minimo': 'Stock mínimo'
    })
    df_inventario = pd.DataFrame.from_records(inventario.values('nombre', 'stock', 'stock_minimo', 'categoria__nombre', 'activo')).rename(columns={
        'nombre': 'Producto',
        'stock': 'Stock',
        'stock_minimo': 'Stock mínimo',
        'categoria__nombre': 'Categoría',
        'activo': 'Activo'
    })

    # Formatear fechas como texto legible
    for df in [df_entradas, df_salidas]:
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha']).dt.tz_localize(None).dt.strftime('%Y-%m-%d %H:%M')

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        hojas = {
            'Entradas': df_entradas,
            'Salidas': df_salidas,
            'Stock Bajo': df_stock_bajo,
            'Inventario Completo': df_inventario,
        }

        for nombre_hoja, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
            ws = writer.sheets[nombre_hoja]
            for idx, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                ws.set_column(idx, idx, max_len)

    output.seek(0)
    filename = f"Resumen_Mes_{now.strftime('%B')}.xlsx"
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

def exportar_inventario_completo(request):
    productos = Producto.objects.all()

    df = pd.DataFrame.from_records(productos.values(
        'nombre', 'stock', 'stock_minimo', 'categoria__nombre', 'activo'
    )).rename(columns={
        'nombre': 'Producto',
        'stock': 'Stock',
        'stock_minimo': 'Stock mínimo',
        'categoria__nombre': 'Categoría',
        'activo': 'Activo'
    })

    # Convertir booleano a texto "Sí"/"No"
    df['Activo'] = df['Activo'].apply(lambda x: 'Sí' if x else 'No')

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Inventario Completo', index=False)

        ws = writer.sheets['Inventario Completo']

        # Ajuste automático de columnas
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            ws.set_column(idx, idx, max_len)

        # Formato condicional: verde para Sí, rojo para No en columna "Activo"
        workbook = writer.book
        formato_si = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        formato_no = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})

        # Suponiendo que la columna "Activo" está en la columna E (índice 4)
        fila_inicio = 2  # Excel comienza en 1, y fila 1 es encabezado
        fila_final = len(df) + 1

        ws.conditional_format(f'E{fila_inicio}:E{fila_final}', {
            'type': 'text',
            'criteria': 'containing',
            'value': 'Sí',
            'format': formato_si
        })
        ws.conditional_format(f'E{fila_inicio}:E{fila_final}', {
            'type': 'text',
            'criteria': 'containing',
            'value': 'No',
            'format': formato_no
        })

    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Inventario_Completo.xlsx'
    return response
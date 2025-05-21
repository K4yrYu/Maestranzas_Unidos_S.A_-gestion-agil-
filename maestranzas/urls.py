from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('principal.urls')), 
    path('productos/', include('producto.urls')), 
    path('usuarios/', include('usuarios.urls')),
    path('movimientos/', include('movimientos.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('ordenes/', include('ordenes_compra.urls')),

]
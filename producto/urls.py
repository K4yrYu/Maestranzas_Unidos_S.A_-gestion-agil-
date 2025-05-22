from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('nuevo/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/exportar-excel/', views.exportar_excel_resumen, name='exportar_excel'),
    path('dashboard/exportar-inventario/', views.exportar_inventario_completo, name='exportar_inventario'),
     path('productos/criticos/', views.productos_criticos, name='productos_criticos'), 




]
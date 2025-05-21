from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proveedores, name='lista_proveedores'),
    path('crear/', views.crear_proveedor, name='crear_proveedor'),
    path('editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('desactivar/<int:id>/', views.desactivar_proveedor, name='desactivar_proveedor'),
    path('reactivar/<int:proveedor_id>/', views.reactivar_proveedor, name='reactivar_proveedor'),  
]
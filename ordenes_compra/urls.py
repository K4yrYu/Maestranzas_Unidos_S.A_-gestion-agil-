from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('crear/', views.crear_orden, name='crear_orden'),
    path('detalle/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('estado/<int:orden_id>/<str:nuevo_estado>/', views.cambiar_estado, name='cambiar_estado'),
    path('crear-desde-criticos/', views.crear_orden_desde_criticos, name='crear_orden_desde_criticos'),  # ✅ NUEVA LÍNEA
]
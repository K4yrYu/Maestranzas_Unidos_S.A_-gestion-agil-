from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_movimientos, name='lista_movimientos'),
    path('nuevo/', views.nuevo_movimiento, name='nuevo_movimiento'),
]

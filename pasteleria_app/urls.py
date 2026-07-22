from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('reportes/', views.reportes, name='reportes'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('inventario/', views.inventario, name='inventario'),
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('mantenimiento/', views.mantenimiento_equipos, name='mantenimiento_equipos'),
]

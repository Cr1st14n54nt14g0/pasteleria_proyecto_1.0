from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('inventario/', views.inventario, name='inventario'),
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('mantenimiento/', views.mantenimiento_equipos, name='mantenimiento_equipos'),
    path('reportes/', views.reportes, name='reportes'),
    path('configuracion/', views.configuracion, name='configuracion'),
    # Usuarios (admin)
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    # Fabricación
    path('producto/<int:producto_id>/producir/', views.producir_producto, name='producir_producto'),
    # Menú público
    path('menu/', views.menu_publico, name='menu_publico'),
    # CRUD de productos, insumos, inventario (si no los tienes, agrégalos)
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    path('insumos/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    path('insumos/<int:pk>/editar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    path('insumos/<int:pk>/eliminar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),
    path('inventario/nuevo/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/<int:pk>/editar/', views.InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario/<int:pk>/eliminar/', views.InventarioDeleteView.as_view(), name='inventario_delete'),
    path('almacen/', views.almacen, name='almacen'),
    
]
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
    path('caja/abrir/', views.abrir_caja, name='abrir_caja'),
    path('caja/cerrar/', views.cerrar_caja, name='cerrar_caja'),
    path('logs/', views.ver_logs, name='ver_logs'),
    path('calcular-insumos/', views.calcular_insumos, name='calcular_insumos'),
    path('calcular-insumos/api/', views.calcular_insumos_api, name='calcular_insumos_api'),
    # Vista unificada de Almacén
    path('almacen/', views.almacen, name='almacen'),

    # CRUD Productos
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # CRUD Insumos
    path('insumos/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    path('insumos/<int:pk>/editar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    path('insumos/<int:pk>/eliminar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),

    # CRUD Inventario
    path('inventario/nuevo/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/<int:pk>/editar/', views.InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario/<int:pk>/eliminar/', views.InventarioDeleteView.as_view(), name='inventario_delete'),
    # Lotes
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    path('lotes/nuevo/', views.crear_lote, name='crear_lote'),
    path('lotes/<int:pk>/eliminar/', views.eliminar_lote, name='eliminar_lote'),

    # Fabricación (ProductoAlmacen)
    path('fabricacion/', views.lista_fabricacion, name='lista_fabricacion'),
    path('fabricacion/nueva/', views.fabricar_producto, name='fabricar_producto'),
    path('fabricacion/<int:pk>/eliminar/', views.eliminar_fabricacion, name='eliminar_fabricacion'),

    # Mostrador
    path('mostrador/', views.lista_mostrador, name='lista_mostrador'),
    path('mostrador/nuevo/', views.agregar_mostrador, name='agregar_mostrador'),
    path('mostrador/<int:pk>/eliminar/', views.eliminar_mostrador, name='eliminar_mostrador'),

    # Fabricación (ProductoAlmacen)
    path('fabricacion/', views.lista_fabricacion, name='lista_fabricacion'),
    path('fabricacion/nueva/', views.fabricar_producto, name='fabricar_producto'),
    path('fabricacion/<int:pk>/eliminar/', views.eliminar_fabricacion, name='eliminar_fabricacion'),

    # Mostrador
    path('mostrador/', views.lista_mostrador, name='lista_mostrador'),
    path('mostrador/nuevo/', views.agregar_mostrador, name='agregar_mostrador'),
    path('mostrador/<int:pk>/eliminar/', views.eliminar_mostrador, name='eliminar_mostrador'),

    path('usuarios/<int:pk>/toggle-activo/', views.toggle_usuario_activo, name='toggle_usuario_activo'),
]
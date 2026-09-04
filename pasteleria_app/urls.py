from django.urls import path
from . import views

urlpatterns = [
    # ========== DASHBOARD ==========
    path('dashboard/', views.dashboard, name='dashboard'),

    # ========== ALMACÉN ==========
    path('almacen/', views.almacen, name='almacen'),

    # Productos
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # Insumos
    path('insumos/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    path('insumos/<int:pk>/editar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    path('insumos/<int:pk>/eliminar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),

    # Inventario
    path('inventario/nuevo/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/<int:pk>/editar/', views.InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario/<int:pk>/eliminar/', views.InventarioDeleteView.as_view(), name='inventario_delete'),

    # ========== LOTES ==========
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    path('lotes/nuevo/', views.crear_lote, name='crear_lote'),
    path('lotes/<int:pk>/eliminar/', views.eliminar_lote, name='eliminar_lote'),

    # ========== FABRICACIÓN ==========
    path('fabricacion/', views.lista_fabricacion, name='lista_fabricacion'),
    path('fabricacion/nueva/', views.fabricar_producto, name='fabricar_producto'),
    path('fabricacion/<int:pk>/eliminar/', views.eliminar_fabricacion, name='eliminar_fabricacion'),

    # ========== MOSTRADOR ==========
    path('mostrador/', views.lista_mostrador, name='lista_mostrador'),
    path('mostrador/nuevo/', views.agregar_mostrador, name='agregar_mostrador'),
    path('mostrador/<int:pk>/eliminar/', views.eliminar_mostrador, name='eliminar_mostrador'),

    # ========== PEDIDOS ==========
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/nuevo/', views.PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/editar/', views.PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedidos/<int:pk>/eliminar/', views.PedidoDeleteView.as_view(), name='pedido_delete'),

    # ========== USUARIOS ==========
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/toggle-activo/', views.toggle_usuario_activo, name='toggle_usuario_activo'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),

    # ========== EQUIPOS ==========
    path('equipos/', views.EquipoListView.as_view(), name='lista_equipos'),
    path('equipos/nuevo/', views.EquipoCreateView.as_view(), name='crear_equipo'),
    path('equipos/<int:pk>/editar/', views.EquipoUpdateView.as_view(), name='editar_equipo'),
    path('equipos/<int:pk>/eliminar/', views.EquipoDeleteView.as_view(), name='eliminar_equipo'),

    # ========== MANTENIMIENTOS ==========
    path('mantenimientos/', views.MantenimientoListView.as_view(), name='lista_mantenimientos'),
    path('mantenimientos/nuevo/', views.MantenimientoCreateView.as_view(), name='crear_mantenimiento'),
    path('mantenimientos/<int:pk>/editar/', views.MantenimientoUpdateView.as_view(), name='editar_mantenimiento'),
    path('mantenimientos/<int:pk>/eliminar/', views.MantenimientoDeleteView.as_view(), name='eliminar_mantenimiento'),

    # ========== CAJA ==========
    path('caja/abrir/', views.abrir_caja, name='abrir_caja'),
    path('caja/cerrar/', views.cerrar_caja, name='cerrar_caja'),
    path('cajas/gestion/', views.gestionar_cajas, name='gestionar_cajas'),

    # ========== REPORTES Y CONFIGURACIÓN ==========
    path('reportes/', views.reportes, name='reportes'),
    path('configuracion/', views.configuracion, name='configuracion'),

    # ========== LOGS ==========
    path('logs/', views.ver_logs, name='ver_logs'),

    # ========== MENÚ PÚBLICO ==========
    path('menu/', views.menu_publico, name='menu_publico'),

    # ========== CÁLCULO DE INSUMOS ==========
    path('calcular-insumos/', views.calcular_insumos, name='calcular_insumos'),
    path('calcular-insumos/api/', views.calcular_insumos_api, name='calcular_insumos_api'),
]
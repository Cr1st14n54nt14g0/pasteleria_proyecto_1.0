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

        # CRUD Productos
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # CRUD Insumos
    path('insumos/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    path('insumos/<int:pk>/editar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    path('insumos/<int:pk>/eliminar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),

    # CRUD Pedidos
    path('pedidos/nuevo/', views.PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/editar/', views.PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedidos/<int:pk>/eliminar/', views.PedidoDeleteView.as_view(), name='pedido_delete'),

    # CRUD Equipos
    path('equipos/nuevo/', views.EquipoCreateView.as_view(), name='equipo_create'),
    path('equipos/<int:pk>/editar/', views.EquipoUpdateView.as_view(), name='equipo_update'),
    path('equipos/<int:pk>/eliminar/', views.EquipoDeleteView.as_view(), name='equipo_delete'),

    # CRUD Mantenimientos
    path('mantenimientos/nuevo/', views.MantenimientoCreateView.as_view(), name='mantenimiento_create'),
    path('mantenimientos/<int:pk>/editar/', views.MantenimientoUpdateView.as_view(), name='mantenimiento_update'),
    path('mantenimientos/<int:pk>/eliminar/', views.MantenimientoDeleteView.as_view(), name='mantenimiento_delete'),

    # CRUD Clientes
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    path('almacen/', views.almacen, name='almacen'),

    # CRUD Inventario
    path('inventario/nuevo/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/<int:pk>/editar/', views.InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario/<int:pk>/eliminar/', views.InventarioDeleteView.as_view(), name='inventario_delete'),

]



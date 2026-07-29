from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Sum, Count, Max, FloatField
from django.db.models.functions import Cast
from .models import (
    DatosPersonales, Productos, Insumos, Pedidos, Ventas, DetalleVenta,
    EquiposDeRefrigeracion, Mantenimientos, Inventario, ProductoInsumos
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .decorators import role_required
from .forms import ProductoForm, InsumoForm, PedidoForm, EquipoForm, MantenimientoForm, DatosPersonalesForm

# ------------------------------------------------------------
# Autenticación
# ------------------------------------------------------------
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contrasena')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render(request, 'registration/login.html', {'error': error})

# ------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------
@login_required
def dashboard(request):
    total_productos = Productos.objects.count()
    total_pedidos = Pedidos.objects.count()
    pedidos_pendientes = Pedidos.objects.filter(estado='pendiente').count()

    # Suma de ventas (campo total es JSONField)
    ingresos = Ventas.objects.annotate(
        total_num=Cast('total', FloatField())
    ).aggregate(
        total=Sum('total_num')
    )['total'] or 0

    pedidos = Pedidos.objects.all().order_by('-fecha_pedido')[:5]

    contexto = {
        'active_page': 'dashboard',
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'ingresos': ingresos,
        'pedidos': pedidos,
    }
    return render(request, 'pasteleria_app/dashboard.html', contexto)

# ------------------------------------------------------------
# Pedidos
# ------------------------------------------------------------
@login_required
def lista_pedidos(request):
    pedidos = Pedidos.objects.all().order_by('-fecha_pedido')
    contexto = {
        'active_page': 'pedidos',
        'pedidos': pedidos,
    }
    return render(request, 'pasteleria_app/lista_pedidos.html', contexto)

# ------------------------------------------------------------
# Productos
# ------------------------------------------------------------
@login_required
def lista_productos(request):
    productos = Productos.objects.all()
    contexto = {
        'active_page': 'productos',
        'productos': productos,
    }
    return render(request, 'pasteleria_app/lista_productos.html', contexto)

# ------------------------------------------------------------
# Clientes (DatosPersonales)
# ------------------------------------------------------------
@login_required
def lista_clientes(request):
    clientes = DatosPersonales.objects.all()
    contexto = {
        'active_page': 'clientes',
        'clientes': clientes,
    }
    return render(request, 'pasteleria_app/lista_clientes.html', contexto)

# ------------------------------------------------------------
# Reportes
# ------------------------------------------------------------
@login_required
def reportes(request):
    total_ventas = Ventas.objects.annotate(
        total_num=Cast('total', FloatField())
    ).aggregate(
        total=Sum('total_num')
    )['total'] or 0

    total_pedidos = Pedidos.objects.count()
    pedidos_estados = Pedidos.objects.values('estado').annotate(total=Count('id_pedido'))
    total_productos = Productos.objects.count()
    total_insumos = Insumos.objects.count()

    contexto = {
        'active_page': 'reportes',
        'total_ventas': total_ventas,
        'total_pedidos': total_pedidos,
        'pedidos_estados': pedidos_estados,
        'total_productos': total_productos,
        'total_insumos': total_insumos,
    }
    return render(request, 'pasteleria_app/reportes.html', contexto)

# ------------------------------------------------------------
# Configuración
# ------------------------------------------------------------
@login_required
def configuracion(request):
    contexto = {
        'active_page': 'configuracion',
    }
    return render(request, 'pasteleria_app/configuracion.html', contexto)

# ------------------------------------------------------------
# Inventario
# ------------------------------------------------------------
@login_required
def inventario(request):
    inventario_items = Inventario.objects.select_related('id_producto', 'id_insumo').all()
    contexto = {
        'active_page': 'inventario',
        'inventario_items': inventario_items,
    }
    return render(request, 'pasteleria_app/inventario.html', contexto)

# ------------------------------------------------------------
# Insumos
# ------------------------------------------------------------
@login_required
def lista_insumos(request):
    insumos = Insumos.objects.all()
    contexto = {
        'active_page': 'insumos',
        'insumos': insumos,
    }
    return render(request, 'pasteleria_app/lista_insumos.html', contexto)

# ------------------------------------------------------------
# Mantenimiento de equipos
# ------------------------------------------------------------
@login_required
def mantenimiento_equipos(request):
    equipos = EquiposDeRefrigeracion.objects.annotate(
        ultimo_mantenimiento=Max('mantenimientos__fecha_mantenimiento')
    )
    contexto = {
        'active_page': 'mantenimiento',
        'equipos': equipos,
    }
    return render(request, 'pasteleria_app/mantenimiento_equipos.html', contexto)

# Mixin para proteger vistas basadas en clase
class RoleRequiredMixin:
    required_roles = []
    @method_decorator(login_required)
    @method_decorator(role_required(required_roles))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# ---------- Productos ----------
class ProductoCreateView(RoleRequiredMixin, CreateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'pasteleria_app/producto_form.html'
    success_url = reverse_lazy('lista_productos')
    required_roles = ['admin', 'trabajador']

class ProductoUpdateView(RoleRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'pasteleria_app/producto_form.html'
    success_url = reverse_lazy('lista_productos')
    required_roles = ['admin', 'trabajador']

class ProductoDeleteView(RoleRequiredMixin, DeleteView):
    model = Productos
    template_name = 'pasteleria_app/producto_confirm_delete.html'
    success_url = reverse_lazy('lista_productos')
    required_roles = ['admin', 'trabajador']

# ---------- Insumos ----------
class InsumoCreateView(RoleRequiredMixin, CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'pasteleria_app/insumo_form.html'
    success_url = reverse_lazy('lista_insumos')
    required_roles = ['admin', 'trabajador']

class InsumoUpdateView(RoleRequiredMixin, UpdateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'pasteleria_app/insumo_form.html'
    success_url = reverse_lazy('lista_insumos')
    required_roles = ['admin', 'trabajador']

class InsumoDeleteView(RoleRequiredMixin, DeleteView):
    model = Insumos
    template_name = 'pasteleria_app/insumo_confirm_delete.html'
    success_url = reverse_lazy('lista_insumos')
    required_roles = ['admin', 'trabajador']

# ---------- Pedidos ----------
class PedidoCreateView(RoleRequiredMixin, CreateView):
    model = Pedidos
    form_class = PedidoForm
    template_name = 'pasteleria_app/pedido_form.html'
    success_url = reverse_lazy('lista_pedidos')
    required_roles = ['admin', 'trabajador']

class PedidoUpdateView(RoleRequiredMixin, UpdateView):
    model = Pedidos
    form_class = PedidoForm
    template_name = 'pasteleria_app/pedido_form.html'
    success_url = reverse_lazy('lista_pedidos')
    required_roles = ['admin', 'trabajador']

class PedidoDeleteView(RoleRequiredMixin, DeleteView):
    model = Pedidos
    template_name = 'pasteleria_app/pedido_confirm_delete.html'
    success_url = reverse_lazy('lista_pedidos')
    required_roles = ['admin', 'trabajador']

# ---------- Equipos ----------
class EquipoCreateView(RoleRequiredMixin, CreateView):
    model = EquiposDeRefrigeracion
    form_class = EquipoForm
    template_name = 'pasteleria_app/equipo_form.html'
    success_url = reverse_lazy('mantenimiento_equipos')
    required_roles = ['admin']

class EquipoUpdateView(RoleRequiredMixin, UpdateView):
    model = EquiposDeRefrigeracion
    form_class = EquipoForm
    template_name = 'pasteleria_app/equipo_form.html'
    success_url = reverse_lazy('mantenimiento_equipos')
    required_roles = ['admin']

class EquipoDeleteView(RoleRequiredMixin, DeleteView):
    model = EquiposDeRefrigeracion
    template_name = 'pasteleria_app/equipo_confirm_delete.html'
    success_url = reverse_lazy('mantenimiento_equipos')
    required_roles = ['admin']

# ---------- Mantenimientos ----------
class MantenimientoCreateView(RoleRequiredMixin, CreateView):
    model = Mantenimientos
    form_class = MantenimientoForm
    template_name = 'pasteleria_app/mantenimiento_form.html'
    success_url = reverse_lazy('mantenimiento_equipos')
    required_roles = ['admin']

class MantenimientoUpdateView(RoleRequiredMixin, UpdateView):
    model = Mantenimientos
    form_class = MantenimientoForm
    template_name = 'pasteleria_app/mantenimiento_form.html'
    success_url = reverse_lazy('mantenimiento_equipos')
    required_roles = ['admin']

class MantenimientoDeleteView(RoleRequiredMixin, DeleteView):
    model = Mantenimientos
    template_name = 'pasteleria_app/mantenimiento_confirm_delete.html'
    success_url = reverse_lazy('mantenimiento_equipos')
    required_roles = ['admin']

# ---------- Clientes (DatosPersonales) ----------
class ClienteCreateView(RoleRequiredMixin, CreateView):
    model = DatosPersonales
    form_class = DatosPersonalesForm
    template_name = 'pasteleria_app/cliente_form.html'
    success_url = reverse_lazy('lista_clientes')
    required_roles = ['admin']

class ClienteUpdateView(RoleRequiredMixin, UpdateView):
    model = DatosPersonales
    form_class = DatosPersonalesForm
    template_name = 'pasteleria_app/cliente_form.html'
    success_url = reverse_lazy('lista_clientes')
    required_roles = ['admin']

class ClienteDeleteView(RoleRequiredMixin, DeleteView):
    model = DatosPersonales
    template_name = 'pasteleria_app/cliente_confirm_delete.html'
    success_url = reverse_lazy('lista_clientes')
    required_roles = ['admin']
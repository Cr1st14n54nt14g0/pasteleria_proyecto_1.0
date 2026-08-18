from .utils import registrar_log
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UsuarioForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.db.models import Sum, Count, Max, FloatField
from django.db.models.functions import Cast
from .models import (
    DatosPersonales, Productos, Insumos, Pedidos, Ventas, DetalleVenta,
    EquiposDeRefrigeracion, Mantenimientos, Inventario, ProductoInsumos,
    Usuarios
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .decorators import role_required
from .forms import ProductoForm, InsumoForm, PedidoForm, EquipoForm, MantenimientoForm, DatosPersonalesForm
from .forms import InventarioForm
from .models import Caja
from django.utils import timezone
from .utils import registrar_log   # solo si creaste utils.py
from .models import Log   # <-- agrega esta línea

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import PermissionDenied

from .models import LoteInsumo, ProductoAlmacen, ProductoMostrador
from .forms import LoteInsumoForm, FabricacionForm, MostradorForm

@login_required
@require_GET
def calcular_insumos_api(request):
    producto_id = request.GET.get('producto_id')
    cantidad = request.GET.get('cantidad', 1)
    try:
        cantidad = int(cantidad)
    except ValueError:
        return JsonResponse({'error': 'Cantidad no válida'}, status=400)

    producto = get_object_or_404(Productos, pk=producto_id)
    insumos = ProductoInsumos.objects.filter(id_producto=producto).select_related('id_insumo')
    data = []
    for item in insumos:
        insumo = item.id_insumo
        total_necesario = item.cantidad * cantidad
        data.append({
            'insumo': insumo.nombre_insumo,
            'unidad': insumo.unidad,
            'cantidad_por_unidad': item.cantidad,
            'total_necesario': total_necesario,
            'stock_actual': insumo.cantidad,
            'suficiente': insumo.cantidad >= total_necesario,
        })
    return JsonResponse({'producto': producto.nombre, 'insumos': data})


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
@role_required(['admin', 'cajero', 'cocinero'])
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
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

class ProductoUpdateView(RoleRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'pasteleria_app/producto_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

class ProductoDeleteView(RoleRequiredMixin, DeleteView):
    model = Productos
    template_name = 'pasteleria_app/producto_confirm_delete.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

# ---------- Insumos ----------
class InsumoCreateView(RoleRequiredMixin, CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'pasteleria_app/insumo_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

class InsumoUpdateView(RoleRequiredMixin, UpdateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'pasteleria_app/insumo_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

class InsumoDeleteView(RoleRequiredMixin, DeleteView):
    model = Insumos
    template_name = 'pasteleria_app/insumo_confirm_delete.html'
    success_url = reverse_lazy('almacen')
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

# ---------- Almacen ----------

@login_required
def almacen(request):
    productos = Productos.objects.all()
    insumos = Insumos.objects.all()
    inventario_items = Inventario.objects.select_related('id_producto', 'id_insumo').all()
    contexto = {
        'active_page': 'almacen',
        'productos': productos,
        'insumos': insumos,
        'inventario_items': inventario_items,
    }
    return render(request, 'pasteleria_app/almacen.html', contexto)

class InventarioCreateView(RoleRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pasteleria_app/inventario_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

class InventarioUpdateView(RoleRequiredMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pasteleria_app/inventario_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

class InventarioDeleteView(RoleRequiredMixin, DeleteView):
    model = Inventario
    template_name = 'pasteleria_app/inventario_confirm_delete.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'trabajador']

@login_required
@role_required(['admin'])
def lista_usuarios(request):
    usuarios = Usuarios.objects.all().select_related('datos_personales')
    contexto = {
        'active_page': 'usuarios',
        'usuarios': usuarios,
    }
    return render(request, 'pasteleria_app/lista_usuarios.html', contexto)

@login_required
@role_required(['admin'])
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.rol == 'admin':
                messages.error(request, "No se puede crear un usuario con rol de administrador.")
                return render(request, 'pasteleria_app/usuario_form.html', {'form': form, 'active_page': 'usuarios'})

            password = form.cleaned_data.get('password')
            if not password:
                messages.error(request, "Debe ingresar una contraseña para el nuevo usuario.")
                return render(request, 'pasteleria_app/usuario_form.html', {'form': form, 'active_page': 'usuarios'})

            user.set_password(password)
            user.is_active = True
            user.is_staff = False
            user.save()

            DatosPersonales.objects.create(
                id_usuario=user.id_usuario,
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion']
            )
            messages.success(request, "Usuario creado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'pasteleria_app/usuario_form.html', {'form': form, 'active_page': 'usuarios'})

@login_required
@role_required(['admin'])
def editar_usuario(request, pk):
    user = get_object_or_404(Usuarios, pk=pk)
    datos = getattr(user, 'datos_personales', None)
    initial = {}
    if datos:
        initial = {
            'nombres': datos.nombres,
            'apellidos': datos.apellidos,
            'telefono': datos.telefono,
            'direccion': datos.direccion,
        }
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user, initial=initial)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            DatosPersonales.objects.update_or_create(
                id_usuario=user.id_usuario,
                defaults={
                    'nombres': form.cleaned_data['nombres'],
                    'apellidos': form.cleaned_data['apellidos'],
                    'telefono': form.cleaned_data['telefono'],
                    'direccion': form.cleaned_data['direccion'],
                }
            )
            messages.success(request, "Usuario actualizado.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=user, initial=initial)
    return render(request, 'pasteleria_app/usuario_form.html', {'form': form, 'active_page': 'usuarios'})

@login_required
@role_required(['admin'])
def eliminar_usuario(request, pk):
    user = get_object_or_404(Usuarios, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('lista_usuarios')
    return render(request, 'pasteleria_app/usuario_confirm_delete.html', {'object': user, 'active_page': 'usuarios'})

# --- Vista de fabricación de producto (descuenta insumos) ---
@login_required
@role_required(['admin', 'cocinero'])
def producir_producto(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    insumos_necesarios = ProductoInsumos.objects.filter(id_producto=producto)
    errores = []
    exito = True

    for item in insumos_necesarios:
        insumo = item.id_insumo
        cantidad_necesaria = item.cantidad
        if insumo.cantidad < cantidad_necesaria:
            errores.append(f"Stock insuficiente de {insumo.nombre_insumo}: necesita {cantidad_necesaria}, hay {insumo.cantidad}.")
            exito = False

    if exito:
        for item in insumos_necesarios:
            insumo = item.id_insumo
            insumo.cantidad -= item.cantidad
            insumo.save()
        messages.success(request, f"Producto '{producto.nombre}' fabricado. Insumos descontados.")
        registrar_log(request.user, 'Fabricación', f'Producto: {producto.nombre}')
    else:
        messages.error(request, "Errores: " + "; ".join(errores))

    return redirect('almacen')

def menu_publico(request):
    productos = Productos.objects.all()   # Sin filtrar por 'disponible'
    return render(request, 'pasteleria_app/menu_publico.html', {'productos': productos})

@login_required
def almacen(request):
    productos = Productos.objects.all()
    insumos = Insumos.objects.all()
    inventario_items = Inventario.objects.select_related('id_producto', 'id_insumo').all()
    contexto = {
        'active_page': 'almacen',
        'productos': productos,
        'insumos': insumos,
        'inventario_items': inventario_items,
    }
    return render(request, 'pasteleria_app/almacen.html', contexto)

@login_required
@role_required(['admin'])
def lista_usuarios(request):
    usuarios = Usuarios.objects.all().select_related('datos_personales')
    contexto = {
        'active_page': 'usuarios',
        'usuarios': usuarios,
    }
    return render(request, 'pasteleria_app/lista_usuarios.html', contexto)

@login_required
@role_required(['admin'])
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Guardar usuario primero para obtener id_usuario (si es nuevo) o actualizar
            user.save()
            # Crear o actualizar DatosPersonales
            datos, created = DatosPersonales.objects.update_or_create(
                id_usuario=user.id_usuario,
                defaults={
                    'nombres': form.cleaned_data.get('nombres', ''),
                    'apellidos': form.cleaned_data.get('apellidos', ''),
                    'telefono': form.cleaned_data.get('telefono', ''),
                    'direccion': form.cleaned_data.get('direccion', ''),
                }
            )
            # Asignar la relación OneToOne (si no existe) desde Usuarios a DatosPersonales
            if not hasattr(user, 'datos_personales') or user.datos_personales is None:
                user.datos_personales = datos
                user.save()
            else:
                # Si ya tenía uno, actualizamos los datos
                user.datos_personales = datos
                user.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'pasteleria_app/usuario_form.html', {
        'form': form,
        'active_page': 'usuarios',
        'titulo': 'Nuevo Usuario'
    })

@login_required
@role_required(['admin'])
def editar_usuario(request, pk):
    user = get_object_or_404(Usuarios, pk=pk)
    datos = getattr(user, 'datos_personales', None)
    initial = {}
    if datos:
        initial = {
            'nombres': datos.nombres,
            'apellidos': datos.apellidos,
            'telefono': datos.telefono,
            'direccion': datos.direccion,
        }
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user, initial=initial)
        if form.is_valid():
            user = form.save()
            # Actualizar DatosPersonales
            datos, created = DatosPersonales.objects.update_or_create(
                id_usuario=user.id_usuario,
                defaults={
                    'nombres': form.cleaned_data.get('nombres', ''),
                    'apellidos': form.cleaned_data.get('apellidos', ''),
                    'telefono': form.cleaned_data.get('telefono', ''),
                    'direccion': form.cleaned_data.get('direccion', ''),
                }
            )
            user.datos_personales = datos
            user.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=user, initial=initial)
    return render(request, 'pasteleria_app/usuario_form.html', {
        'form': form,
        'active_page': 'usuarios',
        'titulo': 'Editar Usuario'
    })

@login_required
@role_required(['admin'])
def eliminar_usuario(request, pk):
    user = get_object_or_404(Usuarios, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('lista_usuarios')
    return render(request, 'pasteleria_app/usuario_confirm_delete.html', {
        'object': user,
        'active_page': 'usuarios'
    })

@login_required
@role_required(['admin', 'cajero'])
def abrir_caja(request):
    # Verificar si ya hay una caja abierta
    if Caja.objects.filter(estado='abierta').exists():
        messages.error(request, "Ya existe una caja abierta. Debe cerrarla antes de abrir otra.")
        return redirect('dashboard')

    if request.method == 'POST':
        monto_inicial = request.POST.get('monto_inicial', 0)
        caja = Caja.objects.create(
            usuario_apertura=request.user,
            monto_inicial=monto_inicial
        )
        messages.success(request, "Caja abierta correctamente.")
        registrar_log(request.user, 'Apertura de caja', f'Monto inicial: {monto_inicial}')
        return redirect('dashboard')

    return render(request, 'pasteleria_app/abrir_caja.html', {'active_page': 'caja'})
    

@login_required
@role_required(['admin', 'cajero'])
def cerrar_caja(request):
    caja_abierta = Caja.objects.filter(estado='abierta').first()
    if not caja_abierta:
        messages.error(request, "No hay ninguna caja abierta.")
        return redirect('dashboard')

    if request.method == 'POST':
        monto_final = request.POST.get('monto_final')
        caja_abierta.monto_final = monto_final
        caja_abierta.fecha_cierre = timezone.now()
        caja_abierta.estado = 'cerrada'
        caja_abierta.save()
        messages.success(request, "Caja cerrada correctamente.")
        registrar_log(request.user, 'Cierre de caja', f'Monto final: {monto_final}')
        return redirect('dashboard')

    return render(request, 'pasteleria_app/cerrar_caja.html', {'caja': caja_abierta, 'active_page': 'caja'})

@login_required
@role_required(['admin'])
def ver_logs(request):
    logs = Log.objects.all()[:100]  # últimos 100 registros
    return render(request, 'pasteleria_app/logs.html', {'logs': logs, 'active_page': 'logs'})

@login_required
@require_GET
def calcular_insumos_api(request):
    producto_id = request.GET.get('producto_id')
    cantidad = request.GET.get('cantidad', 1)
    try:
        cantidad = int(cantidad)
    except ValueError:
        return JsonResponse({'error': 'Cantidad no válida'}, status=400)

    producto = get_object_or_404(Productos, pk=producto_id)
    insumos = ProductoInsumos.objects.filter(id_producto=producto).select_related('id_insumo')
    data = []
    for item in insumos:
        insumo = item.id_insumo
        total_necesario = item.cantidad * cantidad
        data.append({
            'insumo': insumo.nombre_insumo,
            'unidad': insumo.unidad,
            'cantidad_por_unidad': item.cantidad,
            'total_necesario': total_necesario,
            'stock_actual': insumo.cantidad,
            'suficiente': insumo.cantidad >= total_necesario,
        })
    return JsonResponse({'producto': producto.nombre, 'insumos': data})

@login_required
@role_required(['admin', 'cocinero', 'cajero'])
def calcular_insumos(request):
    productos = Productos.objects.all()
    return render(request, 'pasteleria_app/calcular_insumos.html', {
        'productos': productos,
        'active_page': 'calcular_insumos'
    })


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    required_roles = []  # Se define en cada vista

    def test_func(self):
        return self.request.user.rol in self.required_roles

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # Si está autenticado pero no tiene el rol adecuado, error 403
            raise PermissionDenied("No tienes permiso para acceder a esta página.")
        else:
            # Si no está autenticado, redirige al login
            return super().handle_no_permission()

# ---------- Productos ----------
class ProductoCreateView(RoleRequiredMixin, CreateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'pasteleria_app/producto_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

class ProductoUpdateView(RoleRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductoForm
    template_name = 'pasteleria_app/producto_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

class ProductoDeleteView(RoleRequiredMixin, DeleteView):
    model = Productos
    template_name = 'pasteleria_app/producto_confirm_delete.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

# ---------- Insumos ----------
class InsumoCreateView(RoleRequiredMixin, CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'pasteleria_app/insumo_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

class InsumoUpdateView(RoleRequiredMixin, UpdateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'pasteleria_app/insumo_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

class InsumoDeleteView(RoleRequiredMixin, DeleteView):
    model = Insumos
    template_name = 'pasteleria_app/insumo_confirm_delete.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

# ---------- Inventario ----------
class InventarioCreateView(RoleRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pasteleria_app/inventario_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

class InventarioUpdateView(RoleRequiredMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pasteleria_app/inventario_form.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']

class InventarioDeleteView(RoleRequiredMixin, DeleteView):
    model = Inventario
    template_name = 'pasteleria_app/inventario_confirm_delete.html'
    success_url = reverse_lazy('almacen')
    required_roles = ['admin', 'cocinero']


@login_required
@role_required(['admin', 'cocinero'])
def lista_lotes(request):
    lotes = LoteInsumo.objects.select_related('id_insumo').order_by('fecha_caducidad')
    contexto = {
        'active_page': 'lotes',
        'lotes': lotes,
    }
    return render(request, 'pasteleria_app/lista_lotes.html', contexto)

@login_required
@role_required(['admin', 'cocinero'])
def crear_lote(request):
    if request.method == 'POST':
        form = LoteInsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lote creado correctamente.")
            registrar_log(request.user, 'Creación de lote', f"Lote de {form.instance.id_insumo.nombre_insumo}")
            return redirect('lista_lotes')
    else:
        form = LoteInsumoForm()
    return render(request, 'pasteleria_app/lote_form.html', {'form': form, 'active_page': 'lotes'})

@login_required
@role_required(['admin', 'cocinero'])
def eliminar_lote(request, pk):
    lote = get_object_or_404(LoteInsumo, pk=pk)
    if request.method == 'POST':
        insumo = lote.id_insumo.nombre_insumo
        lote.delete()
        messages.success(request, "Lote eliminado.")
        registrar_log(request.user, 'Eliminación de lote', f"Lote de {insumo}")
        return redirect('lista_lotes')
    return render(request, 'pasteleria_app/lote_confirm_delete.html', {'object': lote, 'active_page': 'lotes'})

@login_required
@role_required(['admin', 'cocinero'])
def lista_fabricacion(request):
    fabricaciones = ProductoAlmacen.objects.select_related('id_producto').order_by('-fecha_ingreso')
    contexto = {
        'active_page': 'fabricacion',
        'fabricaciones': fabricaciones,
    }
    return render(request, 'pasteleria_app/lista_fabricacion.html', contexto)

@login_required
@role_required(['admin', 'cocinero'])
def fabricar_producto(request):
    if request.method == 'POST':
        form = FabricacionForm(request.POST)
        if form.is_valid():
            fabricacion = form.save()
            messages.success(request, f"Producto '{fabricacion.id_producto.nombre}' fabricado. Insumos descontados.")
            registrar_log(request.user, 'Fabricación', f"Producto {fabricacion.id_producto.nombre} x{fabricacion.cantidad}")
            return redirect('lista_fabricacion')
    else:
        form = FabricacionForm()
    return render(request, 'pasteleria_app/fabricacion_form.html', {'form': form, 'active_page': 'fabricacion'})

@login_required
@role_required(['admin', 'cocinero'])
def eliminar_fabricacion(request, pk):
    fabricacion = get_object_or_404(ProductoAlmacen, pk=pk)
    if request.method == 'POST':
        producto = fabricacion.id_producto.nombre
        fabricacion.delete()
        messages.success(request, "Registro de fabricación eliminado.")
        registrar_log(request.user, 'Eliminación fabricación', f"{producto} eliminado del almacén")
        return redirect('lista_fabricacion')
    return render(request, 'pasteleria_app/fabricacion_confirm_delete.html', {'object': fabricacion, 'active_page': 'fabricacion'})


@login_required
@role_required(['admin', 'cocinero', 'cajero'])
def lista_mostrador(request):
    mostrador = ProductoMostrador.objects.select_related('id_producto').order_by('-fecha')
    contexto = {
        'active_page': 'mostrador',
        'mostrador': mostrador,
    }
    return render(request, 'pasteleria_app/lista_mostrador.html', contexto)

@login_required
@role_required(['admin', 'cocinero', 'cajero'])
def agregar_mostrador(request):
    if request.method == 'POST':
        form = MostradorForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Producto '{item.id_producto.nombre}' agregado al mostrador.")
            registrar_log(request.user, 'Mostrador', f"{item.id_producto.nombre} x{item.cantidad} en mostrador")
            return redirect('lista_mostrador')
    else:
        form = MostradorForm()
    return render(request, 'pasteleria_app/mostrador_form.html', {'form': form, 'active_page': 'mostrador'})

@login_required
@role_required(['admin', 'cocinero', 'cajero'])
def eliminar_mostrador(request, pk):
    item = get_object_or_404(ProductoMostrador, pk=pk)
    if request.method == 'POST':
        producto = item.id_producto.nombre
        item.delete()
        messages.success(request, "Producto retirado del mostrador.")
        registrar_log(request.user, 'Retiro mostrador', producto)
        return redirect('lista_mostrador')
    return render(request, 'pasteleria_app/mostrador_confirm_delete.html', {'object': item, 'active_page': 'mostrador'})


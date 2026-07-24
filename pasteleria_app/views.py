from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Productos, Pedidos, Ventas
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from .models import EquiposDeRefrigeracion
from django.db.models import Max
from .models import Pedidos
from .models import Inventario
from .models import Productos
from .models import DatosPersonales
from django.db.models import Sum, Count
from .models import Ventas, Pedidos, Productos, Insumos
 
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
 
 
@login_required
def dashboard(request):
    total_productos = Productos.objects.count()
    total_pedidos = Pedidos.objects.count()
    pedidos_pendientes = Pedidos.objects.filter(estado='pendiente').count()

    # Cast del campo JSON 'total' a número antes de sumar
    ingresos = Ventas.objects.annotate(
        total_numerico=Cast('total', FloatField())
    ).aggregate(
        total=Sum('total_numerico')
    )['total'] or 0

    # Últimos 5 pedidos
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

@login_required
def lista_pedidos(request):
    pedidos = Pedidos.objects.all().order_by('-fecha_pedido')
    contexto = {
        'active_page': 'pedidos',
        'pedidos': pedidos,
    }
    return render(request, 'pasteleria_app/lista_pedidos.html', contexto)

@login_required
def inventario(request):
    inventario_items = Inventario.objects.select_related('id_producto', 'id_insumo').all()
    contexto = {
        'active_page': 'inventario',
        'inventario_items': inventario_items,
    }
    return render(request, 'pasteleria_app/inventario.html', contexto)

@login_required
def lista_productos(request):
    productos = Productos.objects.all()
    contexto = {
        'active_page': 'productos',
        'productos': productos,
    }
    return render(request, 'pasteleria_app/lista_productos.html', contexto)

@login_required
def lista_clientes(request):
    clientes = DatosPersonales.objects.all()
    contexto = {
        'active_page': 'clientes',
        'clientes': clientes,
    }
    return render(request, 'pasteleria_app/lista_clientes.html', contexto)

@login_required
def reportes(request):
    # Total de ventas (corregido con Cast)
    total_ventas = Ventas.objects.annotate(
        total_numerico=Cast('total', FloatField())
    ).aggregate(
        total=Sum('total_numerico')
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

@login_required
def configuracion(request):
    # El usuario ya está en request.user (modelo Usuarios)
    contexto = {
        'active_page': 'configuracion',
    }
    return render(request, 'pasteleria_app/configuracion.html', contexto)

@login_required
def lista_insumos(request):
    insumos = Insumos.objects.all()
    contexto = {
        'active_page': 'insumos',
        'insumos': insumos,
    }
    return render(request, 'pasteleria_app/lista_insumos.html', contexto)
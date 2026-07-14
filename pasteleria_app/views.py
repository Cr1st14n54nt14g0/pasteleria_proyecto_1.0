from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required  # si quieres restringir a admins
from django.db.models import Count, Sum
from .models import Productos, Pedidos  # Ajusta los nombres según tus modelos
 
@login_required
def dashboard(request):
    # Estadísticas rápidas para el dashboard
    total_productos = Productos.objects.count()
    total_pedidos = Pedidos.objects.count()
    pedidos_pendientes = Pedidos.objects.filter(estado='pendiente').count()  # Asume que Pedido tiene campo 'estado'
    ingresos = Pedidos.objects.filter(estado='entregado').aggregate(total=Sum('total'))['total'] or 0
    contexto = {
        'active_page': 'dashboard',
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'ingresos': ingresos,
    }
    return render(request, 'pasteleria_app/dashboard.html', contexto)
 
@login_required
def lista_pedidos(request):
    pedidos = Pedidos.objects.all().order_by('-fecha')  # Asume campo 'fecha'
    contexto = {
        'active_page': 'pedidos',
        'pedidos': pedidos,
    }
    return render(request, 'pasteleria_app/lista_pedidos.html', contexto)
 
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
    # Si tienes un modelo Cliente separado, úsalo. Si no, puedes listar usuarios.
    from django.contrib.auth.models import User
    clientes = User.objects.filter(is_staff=False)  # Ejemplo: todos los que no son staff
    contexto = {
        'active_page': 'clientes',
        'clientes': clientes,
    }
    return render(request, 'pasteleria_app/lista_clientes.html', contexto)
 
 
@login_required
def configuracion(request):
    # Página de configuración básica (perfil de usuario)
    contexto = {
        'active_page': 'configuracion',
    }
    return render(request, 'pasteleria_app/configuracion.html', contexto)
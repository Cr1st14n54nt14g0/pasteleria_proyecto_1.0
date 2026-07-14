from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Productos, Pedidos, Ventas
from django.db.models import Sum 
 
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
    ingresos = Ventas.objects.aggregate(total=Sum('total'))['total'] or 0
 
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
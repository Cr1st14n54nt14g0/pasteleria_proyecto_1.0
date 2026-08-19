from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone

 
# ------------------------------------------------------------
# Modelos de negocio
# ------------------------------------------------------------
 
class DatosPersonales(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.JSONField(blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
 
    class Meta:
        db_table = 'datos_personales'
 
 
class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    localizacion = models.CharField(max_length=20, choices=[
        ('mostrador', 'Mostrador'),
        ('pedido', 'Bajo pedido'),
    ], default='mostrador')

    def __str__(self):
        return self.nombre
 
    class Meta:
        db_table = 'productos'
 
 
class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    fecha_venta = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ticket = models.CharField(unique=True, max_length=50)
 
    class Meta:
        db_table = 'ventas'
 
 
class DetalleVenta(models.Model):
    id_venta = models.ForeignKey(Ventas, models.DO_NOTHING, db_column='id_venta')
    id_producto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='id_producto')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    ticket = models.CharField(max_length=50, blank=True, null=True)
 
    class Meta:
        db_table = 'detalle_venta'
 
 
class EquiposDeRefrigeracion(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre_equipo = models.CharField(unique=True, max_length=100)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=17, blank=True, null=True)
 
    class Meta:
        db_table = 'equipos_de_refrigeracion'
 
 
class Insumos(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre_insumo = models.CharField(max_length=100)
    tipo_insumo = models.CharField(max_length=100)
    unidad = models.CharField(max_length=2, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_compra = models.DateField(blank=True, null=True)
    fecha_caducidad = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nombre_insumo
 
    class Meta:
        db_table = 'insumos'
 
 
class Inventario(models.Model):
    id_insumo = models.ForeignKey(Insumos, models.DO_NOTHING, db_column='id_insumo')
    id_producto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='id_producto')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateField(blank=True, null=True)
 
    class Meta:
        db_table = 'inventario'
 
 
class Mantenimientos(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(EquiposDeRefrigeracion, models.DO_NOTHING, db_column='id_equipo')
    id_encargado = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_encargado')
    fecha_mantenimiento = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    proximo_mantenimiento = models.DateField(blank=True, null=True)
 
    class Meta:
        db_table = 'mantenimientos'
 
 
class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField()
    fecha_entrega = models.JSONField(blank=True, null=True)
    estado = models.CharField(max_length=9, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    orden = models.IntegerField(blank=True, null=True)
 
    class Meta:
        db_table = 'pedidos'

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')
    id_producto = models.ForeignKey(Productos, on_delete=models.RESTRICT, db_column='id_producto')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedido'
 
 
class ProductoInsumos(models.Model):
    # Django no soporta claves primarias compuestas, se simula con unique_together
    id_producto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='id_producto')
    id_insumo = models.ForeignKey(Insumos, models.DO_NOTHING, db_column='id_insumo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
 
    class Meta:
        db_table = 'producto_insumos'
        unique_together = (('id_producto', 'id_insumo'),)  # evita duplicados
 
 
# ------------------------------------------------------------
# Modelo de usuario personalizado (reemplaza auth_user)
# ------------------------------------------------------------
 
class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El campo usuario es obligatorio')
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'admin')
        extra_fields.setdefault('estado', 'activo')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(usuario, password, **extra_fields)
 
 
class Usuarios(AbstractBaseUser, PermissionsMixin):
    # Clave primaria propia (AutoField)
    id_usuario = models.AutoField(primary_key=True)
 
    # Relación opcional con DatosPersonales (no es la PK)
    datos_personales = models.OneToOneField(
        DatosPersonales,
        on_delete=models.SET_NULL,
        db_column='id_datos_personales',   # nombre de la columna en la tabla
        null=True,
        blank=True
    )
 
    usuario = models.CharField(unique=True, max_length=50)
    contrasena = models.CharField(max_length=128)  # almacena el hash
    ROLES = [
        ('admin', 'Administrador'),
        ('cajero', 'Cajero'),
        ('cocinero', 'Cocinero/Pastelero'),
        ('ayudante', 'Ayudante'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='ayudante')
    estado = models.CharField(max_length=8, blank=True, null=True, default='activo')
 
    # Campos requeridos por Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_superuser y last_login se heredan de PermissionsMixin y AbstractBaseUser
 
    objects = UsuarioManager()
 
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []
 
    class Meta:
        db_table = 'usuarios'
 
    def __str__(self):
        return self.usuario


class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_column='id_usuario')
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('abierta','Abierta'),('cerrada','Cerrada')], default='abierta')

    class Meta:
        db_table = 'caja'

class MovimientoCaja(models.Model):
    id_movimiento_caja = models.AutoField(primary_key=True)
    id_caja = models.ForeignKey(Caja, on_delete=models.CASCADE, db_column='id_caja', related_name='movimientos')
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_pedido')
    tipo = models.CharField(max_length=15, choices=[
        ('adelanto', 'Adelanto'),
        ('pago_final', 'Pago final'),
        ('otro_ingreso', 'Otro ingreso'),
        ('egreso', 'Egreso'),
    ])
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, db_column='id_usuario')

    class Meta:
        db_table = 'movimientos_caja'

class Log(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha} - {self.usuario} - {self.accion}"


class LoteInsumo(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE, db_column='id_insumo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'lotes_insumos'
        ordering = ['fecha_caducidad', 'id_lote']

    def __str__(self):
        return f"Lote {self.id_lote} de {self.id_insumo.nombre_insumo}"

class ProductoAlmacen(models.Model):
    id_producto_almacen = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, db_column='id_producto')
    id_pedido = models.ForeignKey('Pedidos', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_pedido')
    cantidad = models.PositiveIntegerField(default=0)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=20, default='almacen')

    class Meta:
        db_table = 'producto_almacen'

class ProductoMostrador(models.Model):
    id_producto_mostrador = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, db_column='id_producto')
    id_pedido = models.ForeignKey('Pedidos', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_pedido')
    cantidad = models.PositiveIntegerField(default=1)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'producto_mostrador'

class ConfiguracionCaja(models.Model):
    max_cajas_activas = models.PositiveIntegerField(default=1)
    tiempo_maximo_minutos = models.PositiveIntegerField(default=120)  # 2 horas

    class Meta:
        db_table = 'configuracion_caja'

    def __str__(self):
        return f"Configuración de caja (máx: {self.max_cajas_activas}, tiempo: {self.tiempo_maximo_minutos} min)"

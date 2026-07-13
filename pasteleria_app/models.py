from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class DatosPersonales(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.JSONField(blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'datos_personales'


class DetalleVenta(models.Model):
    id_venta = models.ForeignKey('Ventas', models.DO_NOTHING, db_column='id_venta')
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.JSONField()
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
    cantidad = models.JSONField()
    fecha_compra = models.DateField(blank=True, null=True)
    fecha_caducidad = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'insumos'


class Inventario(models.Model):
    id_insumo = models.ForeignKey(Insumos, models.DO_NOTHING, db_column='id_insumo')
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.JSONField()
    fecha_caducidad = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'inventario'


class Mantenimientos(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(EquiposDeRefrigeracion, models.DO_NOTHING, db_column='id_equipo')
    id_encargado = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_encargado')
    fecha_mantenimiento = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    proximo_mantenimiento = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'mantenimientos'


class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField()
    fecha_entrega = models.JSONField(blank=True, null=True)
    estado = models.CharField(max_length=9, blank=True, null=True)
    total = models.JSONField()
    orden = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pedidos'


class ProductoInsumos(models.Model):
    pk = models.CompositePrimaryKey('id_producto', 'id_insumo')
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    id_insumo = models.ForeignKey(Insumos, models.DO_NOTHING, db_column='id_insumo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'producto_insumos'


class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio = models.JSONField()
    categoria = models.CharField(max_length=50)

    class Meta:
        db_table = 'productos'


class Usuarios(models.Model):
    id_usuario = models.OneToOneField(DatosPersonales, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    usuario = models.CharField(unique=True, max_length=50)
    contrasena = models.CharField(max_length=50)
    rol = models.CharField(max_length=8)
    estado = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'usuarios'


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario')
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    fecha_venta = models.DateTimeField()
    total = models.JSONField()
    ticket = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'ventas'

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import (
    LoteInsumo, Insumos, ProductoAlmacen, ProductoInsumos,
    DetallePedido, Log
)

# --- Estado de insumos (BEFORE INSERT/UPDATE) ---
@receiver(pre_save, sender=Insumos)
def actualizar_estado_insumo(sender, instance, **kwargs):
    if instance.cantidad <= 0:
        instance.estado = 'agotado'
    elif instance.cantidad <= 10:
        instance.estado = 'bajo'
    else:
        instance.estado = 'disponible'

# --- Actualizar stock total en Insumos desde LoteInsumo ---
@receiver([post_save, post_delete], sender=LoteInsumo)
def recalcular_stock_insumos(sender, instance, **kwargs):
    insumo = instance.id_insumo
    total = LoteInsumo.objects.filter(id_insumo=insumo).aggregate(total=Sum('cantidad'))['total'] or 0
    Insumos.objects.filter(pk=insumo.pk).update(cantidad=total)
    # Al hacer update, se dispara pre_save de Insumos y actualiza estado automáticamente.
    # Pero como usamos .update(), no se disparan señales pre_save. Entonces actualizamos estado:
    insumo.refresh_from_db()
    if insumo.cantidad <= 0:
        estado = 'agotado'
    elif insumo.cantidad <= 10:
        estado = 'bajo'
    else:
        estado = 'disponible'
    Insumos.objects.filter(pk=insumo.pk).update(estado=estado)

# --- Consumo FIFO al crear ProductoAlmacen ---
@receiver(post_save, sender=ProductoAlmacen)
def consumo_insumos_almacen(sender, instance, created, **kwargs):
    if created:
        descontar_insumos_fifo(instance.id_producto, instance.cantidad)

# Función auxiliar FIFO
def descontar_insumos_fifo(producto, cantidad_fabricada):
    receta = ProductoInsumos.objects.filter(id_producto=producto)
    for item in receta:
        insumo = item.id_insumo
        cantidad_necesaria = item.cantidad * cantidad_fabricada
        restante = cantidad_necesaria
        lotes = LoteInsumo.objects.filter(id_insumo=insumo, cantidad__gt=0).order_by('fecha_caducidad', 'id_lote')
        for lote in lotes:
            if restante <= 0:
                break
            if lote.cantidad >= restante:
                lote.cantidad -= restante
                lote.save()
                restante = 0
            else:
                restante -= lote.cantidad
                lote.cantidad = 0
                lote.save()
        if restante > 0:
            Log.objects.create(
                accion='Error consumo',
                descripcion=f'Stock insuficiente de {insumo.nombre_insumo} para {producto.nombre}. Faltante: {restante}'
            )
        else:
            Log.objects.create(
                accion='Consumo almacen',
                descripcion=f'Producto {producto.nombre} x{cantidad_fabricada} fabricado. Insumo {insumo.nombre_insumo} descontado.'
            )
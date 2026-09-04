from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Insumos, LoteInsumo, ProductoInsumos, ProductoAlmacen

@receiver(pre_save, sender=Insumos)
def actualizar_estado_insumo(sender, instance, **kwargs):
    if instance.cantidad <= 0:
        instance.estado = 'agotado'
    elif instance.cantidad <= 10:
        instance.estado = 'bajo'
    else:
        instance.estado = 'disponible'

@receiver([post_save, post_delete], sender=LoteInsumo)
def recalcular_stock(sender, instance, **kwargs):
    insumo = instance.id_insumo
    total = LoteInsumo.objects.filter(id_insumo=insumo).aggregate(total=Sum('cantidad'))['total'] or 0
    Insumos.objects.filter(pk=insumo.pk).update(cantidad=total)
    # Actualizar estado según nuevo total
    insumo.refresh_from_db()
    if insumo.cantidad <= 0:
        insumo.estado = 'agotado'
    elif insumo.cantidad <= 10:
        insumo.estado = 'bajo'
    else:
        insumo.estado = 'disponible'
    insumo.save()

@receiver(post_save, sender=ProductoAlmacen)
def descontar_insumos_almacen(sender, instance, created, **kwargs):
    if created:
        producto = instance.id_producto
        cantidad_fabricar = instance.cantidad
        receta = ProductoInsumos.objects.filter(id_producto=producto)
        for item in receta:
            insumo = item.id_insumo
            necesario = item.cantidad * cantidad_fabricar
            restante = necesario
            lotes = LoteInsumo.objects.filter(
                id_insumo=insumo,
                cantidad__gt=0
            ).order_by('fecha_caducidad', 'id_lote')
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
            # Las señales de LoteInsumo actualizarán Insumos.cantidad automáticamente
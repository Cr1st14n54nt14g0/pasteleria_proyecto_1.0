from .models import Log

def registrar_log(usuario, accion, descripcion):
    Log.objects.create(usuario=usuario, accion=accion, descripcion=descripcion)
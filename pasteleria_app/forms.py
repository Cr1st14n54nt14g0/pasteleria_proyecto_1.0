from django import forms
from .models import Productos, Insumos, Pedidos, EquiposDeRefrigeracion, Mantenimientos, DatosPersonales

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'precio', 'categoria']

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = ['nombre_insumo', 'tipo_insumo', 'unidad', 'cantidad', 'fecha_compra', 'fecha_caducidad']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['fecha_pedido', 'fecha_entrega', 'estado', 'total']

class EquipoForm(forms.ModelForm):
    class Meta:
        model = EquiposDeRefrigeracion
        fields = ['nombre_equipo', 'tipo', 'estado']

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimientos
        fields = ['id_equipo', 'id_encargado', 'fecha_mantenimiento', 'descripcion', 'proximo_mantenimiento']

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = ['nombres', 'apellidos', 'telefono', 'direccion']
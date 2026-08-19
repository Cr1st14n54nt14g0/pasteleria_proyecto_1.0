from django import forms
from .models import Productos, Insumos, Pedidos, EquiposDeRefrigeracion, Mantenimientos, DatosPersonales
from .models import Inventario
from django import forms
from .models import Usuarios, DatosPersonales
from .models import LoteInsumo, ProductoAlmacen, ProductoMostrador
from .models import EquiposDeRefrigeracion, Mantenimientos


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

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_producto', 'id_insumo', 'cantidad', 'fecha_caducidad']
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Solo si desea cambiarla."
    )
    nombres = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuarios
        fields = ['usuario', 'rol']  # no incluir 'password' ni 'contrasena'
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        roles_permitidos = [
            ('cajero', 'Cajero'),
            ('cocinero', 'Cocinero/Pastelero'),
            ('ayudante', 'Ayudante'),
        ]
        self.fields['rol'].choices = roles_permitidos
        if self.instance.pk and self.instance.rol == 'admin':
            self.fields['rol'].disabled = True
            self.fields['rol'].choices = [('admin', 'Administrador')] + roles_permitidos

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Dejar en blanco para no cambiarla'}),
        help_text="Solo si desea cambiarla."
    )
    nombres = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuarios
        fields = ['usuario', 'rol']
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        roles_permitidos = [
            ('cajero', 'Cajero'),
            ('cocinero', 'Cocinero/Pastelero'),
            ('ayudante', 'Ayudante'),
        ]
        self.fields['rol'].choices = roles_permitidos
        if self.instance.pk and self.instance.rol == 'admin':
            self.fields['rol'].disabled = True
            self.fields['rol'].choices = [('admin', 'Administrador')] + roles_permitidos


from django import forms
from .models import Productos, Insumos, Inventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'precio', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Tarta de fresa'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción breve del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tartas, Panes, Postres...'
            }),
        }

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = ['nombre_insumo', 'tipo_insumo', 'unidad', 'cantidad', 'fecha_compra', 'fecha_caducidad']
        widgets = {
            'nombre_insumo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Harina'
            }),
            'tipo_insumo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Seco, Lácteo, Fruta'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'kg, L, pz'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_caducidad': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_producto', 'id_insumo', 'cantidad', 'fecha_caducidad']
        widgets = {
            'id_producto': forms.Select(attrs={
                'class': 'form-select',
            }),
            'id_insumo': forms.Select(attrs={
                'class': 'form-select',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_caducidad': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class LoteInsumoForm(forms.ModelForm):
    class Meta:
        model = LoteInsumo
        fields = ['id_insumo', 'cantidad', 'fecha_caducidad']
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }

class FabricacionForm(forms.ModelForm):
    class Meta:
        model = ProductoAlmacen
        fields = ['id_producto', 'cantidad']

class MostradorForm(forms.ModelForm):
    class Meta:
        model = ProductoMostrador
        fields = ['id_producto', 'cantidad', 'id_pedido']
        widgets = {
            'id_pedido': forms.Select(),
        }

class FabricacionForm(forms.ModelForm):
    class Meta:
        model = ProductoAlmacen
        fields = ['id_producto', 'cantidad']

class MostradorForm(forms.ModelForm):
    class Meta:
        model = ProductoMostrador
        fields = ['id_producto', 'cantidad', 'id_pedido']
        widgets = {
            'id_pedido': forms.Select(attrs={'class': 'form-select'}),
        }

class EquipoForm(forms.ModelForm):
    class Meta:
        model = EquiposDeRefrigeracion
        fields = ['nombre_equipo', 'tipo', 'estado']
        widgets = {
            'nombre_equipo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimientos
        fields = ['id_equipo', 'id_encargado', 'fecha_mantenimiento', 'descripcion', 'proximo_mantenimiento']
        widgets = {
            'id_equipo': forms.Select(attrs={'class': 'form-select'}),
            'id_encargado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proximo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
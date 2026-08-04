from django import forms
from .models import Productos, Insumos, Pedidos, EquiposDeRefrigeracion, Mantenimientos, DatosPersonales
from .models import Inventario
from django import forms
from .models import Usuarios, DatosPersonales

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
    # Campos de DatosPersonales
    nombres = forms.CharField(max_length=100, required=False)
    apellidos = forms.CharField(max_length=100, required=False)
    telefono = forms.JSONField(required=False)
    direccion = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Usuarios
        fields = ['usuario', 'rol', 'estado', 'is_active', 'is_staff']
        # is_superuser lo manejamos aparte si se requiere

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear o actualizar DatosPersonales
            datos, created = DatosPersonales.objects.update_or_create(
                id_usuario=user.id_usuario,
                defaults={
                    'nombres': self.cleaned_data.get('nombres', ''),
                    'apellidos': self.cleaned_data.get('apellidos', ''),
                    'telefono': self.cleaned_data.get('telefono'),
                    'direccion': self.cleaned_data.get('direccion', '')
                }
            )
        return user

class UsuarioForm(forms.ModelForm):
    # Campos de DatosPersonales
    nombres = forms.CharField(max_length=100, required=False)
    apellidos = forms.CharField(max_length=100, required=False)
    telefono = forms.CharField(required=False)  # Si es JSON, lo trataremos como texto
    direccion = forms.CharField(max_length=150, required=False)

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(),
        required=False  # No requerido al editar
    )

    class Meta:
        model = Usuarios
        fields = ['usuario', 'rol', 'estado', 'is_active', 'is_staff']
        # Nota: is_superuser no se incluye; solo el admin por defecto lo tiene

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


from django import forms
from .models import Productos, Insumos, Inventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'precio', 'categoria']

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = ['nombre_insumo', 'tipo_insumo', 'unidad', 'cantidad', 'fecha_compra', 'fecha_caducidad']
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_producto', 'id_insumo', 'cantidad', 'fecha_caducidad']
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }
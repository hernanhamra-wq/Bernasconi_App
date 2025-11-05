from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Extiende el formulario de creación para incluir los campos extra del modelo."""

    class Meta(UserCreationForm.Meta):
        model = User
        # Incluimos los campos extra aquí para que aparezcan en el formulario de creación
        fields = ('username', 'email', 'telefono', 'fecha_nacimiento', 'role')

@admin.register(User)
class UsuarioAdmin(UserAdmin):
    # Usar el formulario de creación personalizado para que los campos extra estén presentes
    add_form = CustomUserCreationForm

    # Mostrar los campos extra también en la pantalla de creación (Add user)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'telefono', 'fecha_nacimiento', 'role', 'password1', 'password2'),
        }),
    )

    # Mantener los fieldsets existentes y añadir la sección de información adicional para la edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('telefono', 'fecha_nacimiento', 'role')}),
    )

    # Mostrar también el teléfono en la lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'telefono', 'is_staff')
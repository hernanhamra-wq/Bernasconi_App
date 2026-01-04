from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario


class UsuarioCreateForm(UserCreationForm):
    """Formulario para crear usuarios."""

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'role',
                  'telefono', 'fecha_nacimiento', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'autofocus': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@ejemplo.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })


class UsuarioEditForm(forms.ModelForm):
    """Formulario para editar usuarios (sin cambiar contraseña)."""

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'role',
                  'telefono', 'fecha_nacimiento', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

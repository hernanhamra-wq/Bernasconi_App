from django import forms
from .models import Institucion


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ['nombre', 'tipo_institucion', 'direccion', 'contacto_persona', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la institución',
                'autofocus': True
            }),
            'tipo_institucion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }),
            'contacto_persona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Persona de contacto'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@ejemplo.com'
            }),
        }

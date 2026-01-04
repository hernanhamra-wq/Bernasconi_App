from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre', 'tipo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del material',
                'autofocus': True
            }),
            'tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo (ej: Madera, Metal, Textil)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción (opcional)',
                'rows': 3
            }),
        }

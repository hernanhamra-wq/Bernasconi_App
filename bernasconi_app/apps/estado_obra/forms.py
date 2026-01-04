from django import forms
from .models import EstadoObra


class EstadoObraForm(forms.ModelForm):
    class Meta:
        model = EstadoObra
        fields = ['nombre_estado']
        widgets = {
            'nombre_estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Bueno, Regular, Malo, En restauración',
                'autofocus': True
            }),
        }
        labels = {
            'nombre_estado': 'Nombre del estado'
        }

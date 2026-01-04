from django import forms
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'ficha', 'n_de_prestamo', 'estado',
            'institucion_origen', 'institucion_destino',
            'direccion_destino', 'contacto_destino',
            'fecha_inicio', 'fecha_fin_prevista', 'fecha_devolucion_real',
            'seguro_solicitado', 'costo_traslado',
            'requisitos_especiales', 'observaciones', 'responsable'
        ]
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-control'
            }),
            'n_de_prestamo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de préstamo',
                'autofocus': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'institucion_origen': forms.Select(attrs={
                'class': 'form-control'
            }),
            'institucion_destino': forms.Select(attrs={
                'class': 'form-control'
            }),
            'direccion_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de destino'
            }),
            'contacto_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Persona de contacto'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin_prevista': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_devolucion_real': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'seguro_solicitado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'costo_traslado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'requisitos_especiales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'responsable': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

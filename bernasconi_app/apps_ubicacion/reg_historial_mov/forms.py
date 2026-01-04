from django import forms
from .models import RegHistorialMov


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = RegHistorialMov
        fields = [
            'fk_ficha', 'motivo', 'estado',
            'fk_lugar_origen', 'fk_contenedor_origen',
            'fk_lugar_destino', 'fk_contenedor_destino',
            'fk_estado', 'fk_responsable_mov', 'observaciones'
        ]
        widgets = {
            'fk_ficha': forms.Select(attrs={
                'class': 'form-control'
            }),
            'motivo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_lugar_origen': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_contenedor_origen': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_lugar_destino': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_contenedor_destino': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_responsable_mov': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

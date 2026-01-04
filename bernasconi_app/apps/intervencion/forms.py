from django import forms
from .models import Intervencion


class IntervencionForm(forms.ModelForm):
    class Meta:
        model = Intervencion
        fields = [
            'ficha', 'n_intervencion', 'responsable',
            'fecha_inicio', 'fecha_finalizacion',
            'diagnostico', 'procedimientos', 'materiales_utilizados'
        ]
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-control'
            }),
            'n_intervencion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de intervención'
            }),
            'responsable': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_finalizacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Diagnóstico técnico de la obra'
            }),
            'procedimientos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Procedimientos aplicados'
            }),
            'materiales_utilizados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Materiales utilizados en la intervención'
            }),
        }

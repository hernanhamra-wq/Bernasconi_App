from django import forms
from .models import UbicacionLugar


class UbicacionLugarForm(forms.ModelForm):
    class Meta:
        model = UbicacionLugar
        fields = ['nombre_lugar', 'tipo_lugar', 'permite_contenedores', 'observacion']
        widgets = {
            'nombre_lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Depósito Principal, Sala 1',
                'autofocus': True
            }),
            'tipo_lugar': forms.Select(attrs={
                'class': 'form-control'
            }),
            'permite_contenedores': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones (opcional)',
                'rows': 2
            }),
        }

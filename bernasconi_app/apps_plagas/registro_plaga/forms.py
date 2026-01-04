from django import forms
from .models import RegistroPlaga


class RegistroPlagaForm(forms.ModelForm):
    class Meta:
        model = RegistroPlaga
        fields = [
            'ficha', 'manejo', 'tipologia_plaga', 'fecha_registro',
            'conteo_larvas', 'conteo_esqueletos', 'conteo_incisiones', 'conteo_tapones',
            'observaciones'
        ]
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manejo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipologia_plaga': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_registro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'conteo_larvas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'conteo_esqueletos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'conteo_incisiones': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'conteo_tapones': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

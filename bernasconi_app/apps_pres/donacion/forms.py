from django import forms
from .models import Donacion


class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = [
            'ficha', 'institucion_donante', 'fecha_donacion',
            'condicion_legal', 'valuacion', 'documento_pdf',
            'observaciones', 'responsable'
        ]
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-control'
            }),
            'institucion_donante': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_donacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'condicion_legal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'valuacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'documento_pdf': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'responsable': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

from django import forms
from .models import SeguimientoXilofago


class SeguimientoXilofagoForm(forms.ModelForm):
    class Meta:
        model = SeguimientoXilofago
        fields = ['registro_plaga', 'fecha_seguimiento', 'observacion', 'nueva_actividad']
        widgets = {
            'registro_plaga': forms.Select(attrs={'class': 'form-control'}),
            'fecha_seguimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'nueva_actividad': forms.Select(
                attrs={'class': 'form-control'},
                choices=[('', '-- Seleccionar --'), ('baja', 'Baja'), ('alta', 'Alta'), ('nula', 'Nula')]
            ),
        }

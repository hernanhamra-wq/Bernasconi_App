from django import forms
from .models import ContenedorUbicacion
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar


class ContenedorForm(forms.ModelForm):
    class Meta:
        model = ContenedorUbicacion
        fields = [
            'nombre_contenedor', 'fk_lugar_general', 'fk_padre',
            'tipo_contenedor', 'modo_almacenamiento',
            'capacidad_maxima', 'estado', 'observacion'
        ]
        widgets = {
            'nombre_contenedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cajón A-01, Vitrina Norte',
                'autofocus': True
            }),
            'fk_lugar_general': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fk_padre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo_contenedor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'modo_almacenamiento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'capacidad_maxima': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones (opcional)',
                'rows': 2
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar lugares que permiten contenedores
        self.fields['fk_lugar_general'].queryset = UbicacionLugar.objects.filter(
            permite_contenedores=True
        ).order_by('nombre_lugar')
        # Contenedor padre es opcional
        self.fields['fk_padre'].required = False
        self.fields['fk_padre'].queryset = ContenedorUbicacion.objects.order_by('nombre_contenedor')

from django import forms
from .models import FichaTecnica

class FichaTecnicaForm(forms.ModelForm):
    class Meta:
        model = FichaTecnica
        fields = '__all__'
        labels = {
            'n_de_ficha': 'N° de Ficha',
            'inventario': 'Inventario',
            'n_de_inventario_anterior': 'N° Inventario anterior',
            'anio': 'Año',
            'dimensiones': 'Dimensiones (texto)',
            'fk_estado': 'Estado de la obra',
            'fk_responsable_carga': 'Responsable de carga',
            'fk_serie': 'Serie',
            'fk_multimedia_principal': 'Imagen principal',
            'seguimiento': 'Requiere seguimiento',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'observacion': forms.Textarea(attrs={'rows': 3}),
            'dimensiones': forms.Textarea(attrs={'rows': 2}),
        }

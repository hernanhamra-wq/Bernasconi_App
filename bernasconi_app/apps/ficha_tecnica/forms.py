from django import forms
from .models import FichaTecnica
from apps.material.models import Material


class FichaTecnicaForm(forms.ModelForm):

    # ✅ Materiales como checklist (en vez de select chiquito)
    materiales = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Materiales"
    )

    class Meta:
        model = FichaTecnica
        fields = '__all__'

        labels = {
            'n_de_ficha': 'N° de Ficha',
            'inventario': 'Inventario',
            'n_de_inventario_anterior': 'N° Inventario anterior',
            'titulo': 'Título',
            'anio': 'Año',
            'dimensiones': 'Dimensiones (texto)',
            'fk_estado': 'Estado de la obra',
            'fk_responsable_carga': 'Responsable de carga',
            'fk_serie': 'Serie',
            'fk_multimedia_principal': 'Imagen principal',
            'seguimiento': 'Requiere seguimiento',
            'descripcion': 'Descripción',
            'observacion': 'Observación',
        }

        widgets = {
            'n_de_inventario_anterior': forms.TextInput(),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'observacion': forms.Textarea(attrs={'rows': 3}),
            'dimensiones': forms.Textarea(attrs={'rows': 2}),
        }

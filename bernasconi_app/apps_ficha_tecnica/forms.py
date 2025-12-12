from django import forms
from apps.ficha_tecnica.models import FichaTecnica
from apps.autor.models import Autor


class FichaTecnicaForm(forms.ModelForm):
    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        required=False,
        widget=forms.SelectMultiple
    )

    class Meta:
        model = FichaTecnica
        fields = [
            'n_de_ficha',
            'inventario',
            'n_de_inventario_anterior',
            'titulo',
            'anio',
            'ancho',
            'alto',
            'diametro',
            'profundidad',
            'descripcion',
            'observacion',
            'fk_estado',
            'fk_serie',
        ]

"""
CRUD de Materiales usando el mixin genérico.
"""

from django.db.models import Count
from apps.core.crud_views import CRUDViewMixin
from .models import Material
from .forms import MaterialForm


class MaterialViews(CRUDViewMixin):
    model = Material
    form_class = MaterialForm
    app_name = 'material'
    model_verbose = 'Material'
    model_verbose_plural = 'Materiales'

    # Búsqueda
    search_fields = ['nombre', 'tipo', 'descripcion']

    # Columnas de la lista
    list_columns = [
        {'field': 'nombre', 'label': 'Nombre', 'is_link': True},
        {'field': 'tipo', 'label': 'Tipo'},
        {'field': 'num_fichas', 'label': 'Fichas', 'is_count': True},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'nombre', 'label': 'Nombre'},
        {'field': 'tipo', 'label': 'Tipo'},
        {'field': 'descripcion', 'label': 'Descripción', 'full_width': True},
    ]

    def get_queryset(self):
        """Añadir conteo de fichas."""
        return self.model.objects.annotate(
            num_fichas=Count('fichas_relacion')
        ).order_by('nombre')

    def can_delete(self, obj):
        """No permitir eliminar si tiene fichas asociadas."""
        num_fichas = obj.fichas_relacion.count()
        if num_fichas > 0:
            return False, [f'{num_fichas} ficha(s) técnica(s) asociada(s)']
        return True, []

    def get_detail_sections(self, obj):
        """Mostrar fichas del material."""
        fichas_rel = obj.fichas_relacion.select_related('ficha').order_by('-ficha__id')[:20]

        return [{
            'title': 'Fichas Técnicas',
            'items': [fr.ficha for fr in fichas_rel],
            'columns': [
                {'field': 'inventario', 'label': 'Inventario'},
                {'field': 'titulo', 'label': 'Título'},
            ],
            'empty_text': 'Este material no tiene fichas asociadas.',
            'action_url': 'ficha_tecnica:ficha_tecnica_detail',
            'action_label': 'Ver ficha',
        }]


# Instancia para usar en urls.py
material_views = MaterialViews()

"""
CRUD de Autores usando el mixin genérico.
"""

from django.db.models import Count
from apps.core.crud_views import CRUDViewMixin
from .models import Autor
from .forms import AutorForm


class AutorViews(CRUDViewMixin):
    model = Autor
    form_class = AutorForm
    app_name = 'autor'

    # Búsqueda
    search_fields = ['nombre', 'biografia']

    # Columnas de la lista
    list_columns = [
        {'field': 'nombre', 'label': 'Nombre', 'is_link': True},
        {'field': 'biografia', 'label': 'Biografía', 'truncate': True},
        {'field': 'num_fichas', 'label': 'Fichas', 'is_count': True},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'nombre', 'label': 'Nombre'},
        {'field': 'biografia', 'label': 'Biografía', 'full_width': True},
    ]

    def get_queryset(self):
        """Añadir conteo de fichas."""
        return self.model.objects.annotate(
            num_fichas=Count('fichaautor')
        ).order_by('nombre')

    def can_delete(self, obj):
        """No permitir eliminar si tiene fichas asociadas."""
        num_fichas = obj.fichaautor_set.count()
        if num_fichas > 0:
            return False, [f'{num_fichas} ficha(s) técnica(s) asociada(s)']
        return True, []

    def get_detail_sections(self, obj):
        """Mostrar fichas del autor."""
        fichas_rel = obj.fichaautor_set.select_related('fk_ficha').order_by('-fk_ficha__id')[:20]

        return [{
            'title': 'Fichas Técnicas',
            'items': [fa.fk_ficha for fa in fichas_rel],
            'columns': [
                {'field': 'inventario', 'label': 'Inventario'},
                {'field': 'titulo', 'label': 'Título'},
            ],
            'empty_text': 'Este autor no tiene fichas asociadas.',
            'action_url': 'ficha_tecnica:ficha_tecnica_detail',
            'action_label': 'Ver ficha',
        }]


# Instancia para usar en urls.py
autor_views = AutorViews()

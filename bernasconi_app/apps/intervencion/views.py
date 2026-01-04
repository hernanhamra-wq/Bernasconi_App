"""
CRUD de Intervenciones (Restauraciones) usando el mixin genérico.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import Intervencion
from .forms import IntervencionForm


class IntervencionViews(CRUDViewMixin):
    model = Intervencion
    form_class = IntervencionForm
    app_name = 'intervencion'
    model_verbose = 'Intervención'
    model_verbose_plural = 'Intervenciones'
    page_bg_class = 'bg-conservacion'
    form_max_width = '800px'

    # Búsqueda
    search_fields = ['ficha__inventario', 'ficha__titulo', 'diagnostico']

    # Columnas de la lista
    list_columns = [
        {'field': 'n_intervencion', 'label': 'N°', 'is_link': True},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'responsable', 'label': 'Responsable'},
        {'field': 'fecha_inicio', 'label': 'Inicio'},
        {'field': 'fecha_finalizacion', 'label': 'Fin'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'intervencion_id', 'label': 'ID'},
        {'field': 'n_intervencion', 'label': 'N° Intervención'},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'responsable', 'label': 'Responsable'},
        {'field': 'fecha_inicio', 'label': 'Fecha Inicio'},
        {'field': 'fecha_finalizacion', 'label': 'Fecha Finalización'},
        {'field': 'diagnostico', 'label': 'Diagnóstico Técnico', 'full_width': True},
        {'field': 'procedimientos', 'label': 'Procedimientos Aplicados', 'full_width': True},
        {'field': 'materiales_utilizados', 'label': 'Materiales Utilizados', 'full_width': True},
    ]

    def can_delete(self, obj):
        """Siempre se puede eliminar una intervención."""
        return True, []


# Instancia para usar en urls.py
intervencion_views = IntervencionViews()

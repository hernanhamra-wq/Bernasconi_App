"""
CRUD de Donaciones usando el mixin genérico.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import Donacion
from .forms import DonacionForm


class DonacionViews(CRUDViewMixin):
    model = Donacion
    form_class = DonacionForm
    app_name = 'donacion'
    model_verbose = 'Donación'
    model_verbose_plural = 'Donaciones'
    page_bg_class = 'bg-prestamos'
    form_max_width = '700px'

    # Búsqueda
    search_fields = ['ficha__inventario', 'ficha__titulo', 'institucion_donante__nombre']

    # Filtros
    filters = [
        {
            'name': 'condicion',
            'label': 'Condición Legal',
            'field': 'condicion_legal',
            'choices': Donacion.CONDICION_LEGAL_CHOICES,
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'ficha', 'label': 'Obra', 'is_link': True},
        {'field': 'institucion_donante', 'label': 'Donante'},
        {'field': 'fecha_donacion', 'label': 'Fecha'},
        {'field': 'get_condicion_legal_display', 'label': 'Condición', 'is_badge': True, 'badge_class': 'primary'},
        {'field': 'valuacion', 'label': 'Valuación'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'institucion_donante', 'label': 'Institución Donante'},
        {'field': 'fecha_donacion', 'label': 'Fecha de Donación'},
        {'field': 'get_condicion_legal_display', 'label': 'Condición Legal', 'is_badge': True},
        {'field': 'valuacion', 'label': 'Valuación'},
        {'field': 'documento_pdf', 'label': 'Documento PDF'},
        {'field': 'observaciones', 'label': 'Observaciones', 'full_width': True},
        {'field': 'responsable', 'label': 'Responsable'},
    ]

    def can_delete(self, obj):
        """Siempre se puede eliminar una donación."""
        return True, []


# Instancia para usar en urls.py
donacion_views = DonacionViews()

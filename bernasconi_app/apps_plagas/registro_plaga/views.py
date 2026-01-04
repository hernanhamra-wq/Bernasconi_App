"""
CRUD de Registros de Plagas usando el mixin genérico.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import RegistroPlaga
from .forms import RegistroPlagaForm


class RegistroPlagaViews(CRUDViewMixin):
    model = RegistroPlaga
    form_class = RegistroPlagaForm
    app_name = 'registro_plaga'
    model_verbose = 'Registro de Plaga'
    model_verbose_plural = 'Registros de Plagas'
    page_bg_class = 'bg-plagas'
    form_max_width = '700px'

    # Búsqueda
    search_fields = ['ficha__inventario', 'ficha__titulo', 'observaciones']

    # Columnas de la lista
    list_columns = [
        {'field': 'registro_id', 'label': 'ID', 'is_link': True},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'tipologia_plaga', 'label': 'Tipo Plaga'},
        {'field': 'fecha_registro', 'label': 'Fecha'},
        {'field': 'conteo_larvas', 'label': 'Larvas'},
        {'field': 'conteo_incisiones', 'label': 'Incisiones'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'registro_id', 'label': 'ID'},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'tipologia_plaga', 'label': 'Tipo de Plaga'},
        {'field': 'manejo', 'label': 'Plan de Manejo'},
        {'field': 'fecha_registro', 'label': 'Fecha de Registro'},
        {'field': 'conteo_larvas', 'label': 'Conteo de Larvas'},
        {'field': 'conteo_esqueletos', 'label': 'Conteo de Esqueletos'},
        {'field': 'conteo_incisiones', 'label': 'Conteo de Incisiones'},
        {'field': 'conteo_tapones', 'label': 'Conteo de Tapones'},
        {'field': 'observaciones', 'label': 'Observaciones', 'full_width': True},
        {'field': 'usuario_registro', 'label': 'Registrado por'},
    ]

    def can_delete(self, obj):
        """Siempre se puede eliminar un registro de plaga."""
        return True, []


# Instancia para usar en urls.py
registro_plaga_views = RegistroPlagaViews()

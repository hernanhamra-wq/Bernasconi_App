"""
CRUD de Seguimiento de Xilófagos.
Permite registrar y hacer seguimiento de plagas detectadas.
"""

from django.db.models import Count
from apps.core.crud_views import CRUDViewMixin
from .models import SeguimientoXilofago
from .forms import SeguimientoXilofagoForm


class SeguimientoXilofagoViews(CRUDViewMixin):
    model = SeguimientoXilofago
    form_class = SeguimientoXilofagoForm
    app_name = 'seguimiento_xilofago'
    model_verbose = 'Seguimiento Xilófago'
    model_verbose_plural = 'Seguimientos Xilófagos'
    page_bg_class = 'bg-plagas'

    # Búsqueda
    search_fields = ['observacion', 'registro_plaga__ficha__titulo', 'registro_plaga__ficha__inventario']

    # Filtros
    filters = [
        {
            'name': 'actividad',
            'label': 'Actividad',
            'field': 'nueva_actividad',
            'choices': [('baja', 'Baja'), ('alta', 'Alta'), ('nula', 'Nula')]
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'registro_plaga', 'label': 'Registro Plaga', 'is_link': True},
        {'field': 'fecha_seguimiento', 'label': 'Fecha'},
        {'field': 'nueva_actividad', 'label': 'Actividad'},
        {'field': 'observacion', 'label': 'Observación', 'truncate': True},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'seguimiento_id', 'label': 'ID'},
        {'field': 'registro_plaga', 'label': 'Registro Plaga'},
        {'field': 'fecha_seguimiento', 'label': 'Fecha Seguimiento'},
        {'field': 'nueva_actividad', 'label': 'Nueva Actividad'},
        {'field': 'observacion', 'label': 'Observación'},
        {'field': 'usuario_registro', 'label': 'Usuario Registro'},
    ]

    def get_queryset(self):
        return self.model.objects.select_related(
            'registro_plaga',
            'registro_plaga__ficha',
            'usuario_registro'
        ).order_by('-fecha_seguimiento')

    def get_initial_data(self, request):
        """Pre-llenar registro_plaga si viene en el URL."""
        initial = {}
        registro_id = request.GET.get('registro_plaga')
        if registro_id:
            initial['registro_plaga'] = registro_id
        return initial


# Instancia para urls.py
seguimiento_xilofago_views = SeguimientoXilofagoViews()

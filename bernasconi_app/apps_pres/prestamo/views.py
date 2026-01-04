"""
CRUD de Préstamos usando el mixin genérico.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import Prestamo
from .forms import PrestamoForm


class PrestamoViews(CRUDViewMixin):
    model = Prestamo
    form_class = PrestamoForm
    app_name = 'prestamo'
    model_verbose = 'Préstamo'
    model_verbose_plural = 'Préstamos'
    page_bg_class = 'bg-prestamos'
    form_max_width = '800px'

    # Búsqueda
    search_fields = ['n_de_prestamo', 'ficha__inventario', 'ficha__titulo']

    # Filtros
    filters = [
        {
            'name': 'estado',
            'label': 'Estado',
            'field': 'estado',
            'choices': Prestamo.ESTADO_CHOICES,
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'n_de_prestamo', 'label': 'N° Préstamo', 'is_link': True},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'institucion_destino', 'label': 'Destino'},
        {'field': 'fecha_inicio', 'label': 'Inicio'},
        {'field': 'fecha_fin_prevista', 'label': 'Fin Previsto'},
        {'field': 'get_estado_display', 'label': 'Estado', 'is_badge': True, 'badge_class': 'info'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'n_de_prestamo', 'label': 'N° Préstamo'},
        {'field': 'ficha', 'label': 'Obra'},
        {'field': 'get_estado_display', 'label': 'Estado', 'is_badge': True},
        {'field': 'institucion_origen', 'label': 'Institución Origen'},
        {'field': 'institucion_destino', 'label': 'Institución Destino'},
        {'field': 'direccion_destino', 'label': 'Dirección Destino', 'full_width': True},
        {'field': 'contacto_destino', 'label': 'Contacto'},
        {'field': 'fecha_inicio', 'label': 'Fecha Inicio'},
        {'field': 'fecha_fin_prevista', 'label': 'Fecha Fin Prevista'},
        {'field': 'fecha_devolucion_real', 'label': 'Fecha Devolución Real'},
        {'field': 'seguro_solicitado', 'label': 'Seguro Solicitado'},
        {'field': 'costo_traslado', 'label': 'Costo Traslado'},
        {'field': 'requisitos_especiales', 'label': 'Requisitos Especiales', 'full_width': True},
        {'field': 'observaciones', 'label': 'Observaciones', 'full_width': True},
        {'field': 'responsable', 'label': 'Responsable'},
    ]

    def can_delete(self, obj):
        """Permitir eliminar solo si está cancelado o devuelto."""
        if obj.estado in ['CANCELADO', 'DEVUELTO']:
            return True, []
        return False, [f'El préstamo está en estado "{obj.get_estado_display()}"']


# Instancia para usar en urls.py
prestamo_views = PrestamoViews()

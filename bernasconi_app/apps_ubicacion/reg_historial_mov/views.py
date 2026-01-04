"""
CRUD de Movimientos de Obras usando el mixin genérico.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import RegHistorialMov
from .forms import MovimientoForm


class MovimientoViews(CRUDViewMixin):
    model = RegHistorialMov
    form_class = MovimientoForm
    app_name = 'movimiento'
    model_verbose = 'Movimiento'
    model_verbose_plural = 'Movimientos'
    page_bg_class = 'bg-ubicaciones'
    form_max_width = '800px'

    # Búsqueda
    search_fields = ['fk_ficha__inventario', 'fk_ficha__titulo', 'observaciones']

    # Filtros
    filters = [
        {
            'name': 'motivo',
            'label': 'Motivo',
            'field': 'motivo',
            'choices': RegHistorialMov.MOTIVO_CHOICES,
        },
        {
            'name': 'estado',
            'label': 'Estado',
            'field': 'estado',
            'choices': RegHistorialMov.ESTADO_MOVIMIENTO_CHOICES,
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'id', 'label': 'ID', 'is_link': True},
        {'field': 'fk_ficha', 'label': 'Obra'},
        {'field': 'fk_lugar_destino', 'label': 'Destino'},
        {'field': 'get_motivo_display', 'label': 'Motivo', 'is_badge': True, 'badge_class': 'info'},
        {'field': 'get_estado_display', 'label': 'Estado', 'is_badge': True, 'badge_class': 'primary'},
        {'field': 'fecha_movimiento', 'label': 'Fecha'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'fk_ficha', 'label': 'Obra'},
        {'field': 'get_motivo_display', 'label': 'Motivo', 'is_badge': True},
        {'field': 'get_estado_display', 'label': 'Estado del Movimiento', 'is_badge': True},
        {'field': 'fk_lugar_origen', 'label': 'Lugar de Origen'},
        {'field': 'fk_contenedor_origen', 'label': 'Contenedor de Origen'},
        {'field': 'fk_lugar_destino', 'label': 'Lugar de Destino'},
        {'field': 'fk_contenedor_destino', 'label': 'Contenedor de Destino'},
        {'field': 'fk_estado', 'label': 'Condición de la Obra'},
        {'field': 'fecha_movimiento', 'label': 'Fecha del Movimiento'},
        {'field': 'fk_responsable_mov', 'label': 'Responsable'},
        {'field': 'observaciones', 'label': 'Observaciones', 'full_width': True},
    ]

    def get_queryset(self):
        """Ordenar por fecha descendente."""
        return self.model.objects.all().order_by('-fecha_movimiento')

    def can_delete(self, obj):
        """Solo permitir eliminar movimientos cancelados."""
        if obj.estado == 'CANCELADO':
            return True, []
        return False, [f'Solo se pueden eliminar movimientos cancelados. Estado actual: {obj.get_estado_display()}']


# Instancia para usar en urls.py
movimiento_views = MovimientoViews()

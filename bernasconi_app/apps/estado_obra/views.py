"""
CRUD de Situaciones de Obra usando el mixin genérico.
Representa la situación operativa: Exposición, Depósito, Cuarentena, etc.
"""

from django.db.models import Count
from apps.core.crud_views import CRUDViewMixin
from .models import EstadoObra
from .forms import EstadoObraForm


class EstadoObraViews(CRUDViewMixin):
    model = EstadoObra
    form_class = EstadoObraForm
    app_name = 'estado_obra'
    model_verbose = 'Situación'
    model_verbose_plural = 'Situaciones'
    page_bg_class = 'bg-ubicaciones'

    # Búsqueda
    search_fields = ['nombre_estado']

    # Columnas de la lista
    list_columns = [
        {'field': 'nombre_estado', 'label': 'Situación', 'is_link': True},
        {'field': 'num_fichas', 'label': 'Fichas', 'is_count': True},
        {'field': 'num_movimientos', 'label': 'Movimientos', 'is_count': True},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'nombre_estado', 'label': 'Situación'},
    ]

    def get_queryset(self):
        """Añadir conteos."""
        return self.model.objects.annotate(
            num_fichas=Count('fichatecnica'),
            num_movimientos=Count('historial_movimientos')
        ).order_by('nombre_estado')

    def can_delete(self, obj):
        """No permitir eliminar si está en uso."""
        num_fichas = obj.fichatecnica_set.count()
        num_movimientos = obj.historial_movimientos.count()
        reasons = []
        if num_fichas > 0:
            reasons.append(f'{num_fichas} ficha(s) técnica(s)')
        if num_movimientos > 0:
            reasons.append(f'{num_movimientos} movimiento(s)')
        return len(reasons) == 0, reasons


# Instancia para usar en urls.py
estado_obra_views = EstadoObraViews()

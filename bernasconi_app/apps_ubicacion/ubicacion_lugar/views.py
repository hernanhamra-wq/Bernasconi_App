"""
CRUD de Lugares (Ubicaciones) usando el mixin genérico.
"""

from django.db.models import Count
from apps.core.crud_views import CRUDViewMixin
from .models import UbicacionLugar
from .forms import UbicacionLugarForm


class LugarViews(CRUDViewMixin):
    model = UbicacionLugar
    form_class = UbicacionLugarForm
    app_name = 'ubicacion'
    model_verbose = 'Lugar'
    model_verbose_plural = 'Lugares'
    page_bg_class = 'bg-ubicaciones'

    # Búsqueda
    search_fields = ['nombre_lugar', 'observacion']

    # Filtros
    filters = [
        {
            'name': 'tipo',
            'label': 'Tipo',
            'field': 'tipo_lugar',
            'choices': UbicacionLugar.TIPO_LUGAR_CHOICES,
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'nombre_lugar', 'label': 'Nombre', 'is_link': True},
        {'field': 'get_tipo_lugar_display', 'label': 'Tipo', 'is_badge': True, 'badge_class': 'info'},
        {'field': 'permite_contenedores', 'label': 'Contenedores'},
        {'field': 'num_contenedores', 'label': 'Cant.', 'is_count': True},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'nombre_lugar', 'label': 'Nombre'},
        {'field': 'get_tipo_lugar_display', 'label': 'Tipo', 'is_badge': True},
        {'field': 'permite_contenedores', 'label': 'Permite Contenedores'},
        {'field': 'observacion', 'label': 'Observaciones', 'full_width': True},
    ]

    def get_queryset(self):
        """Añadir conteos."""
        return self.model.objects.annotate(
            num_contenedores=Count('contenedorubicacion'),
            num_movimientos_destino=Count('historial_movimientos_destino')
        ).order_by('nombre_lugar')

    def can_delete(self, obj):
        """No permitir eliminar si está en uso."""
        num_contenedores = obj.contenedorubicacion_set.count()
        num_movimientos = obj.historial_movimientos_destino.count()
        reasons = []
        if num_contenedores > 0:
            reasons.append(f'{num_contenedores} contenedor(es)')
        if num_movimientos > 0:
            reasons.append(f'{num_movimientos} movimiento(s)')
        return len(reasons) == 0, reasons

    def get_detail_sections(self, obj):
        """Mostrar contenedores del lugar."""
        contenedores = obj.contenedorubicacion_set.filter(fk_padre__isnull=True).order_by('nombre_contenedor')

        return [{
            'title': 'Contenedores',
            'items': list(contenedores),
            'columns': [
                {'field': 'nombre_contenedor', 'label': 'Nombre'},
                {'field': 'get_tipo_contenedor_display', 'label': 'Tipo'},
                {'field': 'get_estado_display', 'label': 'Estado'},
            ],
            'empty_text': 'Este lugar no tiene contenedores.',
            'action_url': 'contenedor:contenedor_detail',
            'action_label': 'Ver',
            'add_url': 'contenedor:contenedor_create',
            'add_label': 'Agregar Contenedor',
            'add_params': f'lugar={obj.pk}',
        }]


# Instancia para usar en urls.py
lugar_views = LugarViews()

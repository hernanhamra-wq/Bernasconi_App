"""
CRUD de Contenedores usando el mixin genérico.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import ContenedorUbicacion
from .forms import ContenedorForm
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar


class ContenedorViews(CRUDViewMixin):
    model = ContenedorUbicacion
    form_class = ContenedorForm
    app_name = 'contenedor'
    model_verbose = 'Contenedor'
    model_verbose_plural = 'Contenedores'
    page_bg_class = 'bg-ubicaciones'

    # Búsqueda
    search_fields = ['nombre_contenedor', 'observacion']

    # Filtros
    filters = [
        {
            'name': 'tipo',
            'label': 'Tipo',
            'field': 'tipo_contenedor',
            'choices': ContenedorUbicacion.TIPO_CONTENEDOR,
        },
        {
            'name': 'estado',
            'label': 'Estado',
            'field': 'estado',
            'choices': ContenedorUbicacion.ESTADO_CONTENEDOR,
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'nombre_contenedor', 'label': 'Nombre', 'is_link': True},
        {'field': 'fk_lugar_general', 'label': 'Lugar'},
        {'field': 'get_tipo_contenedor_display', 'label': 'Tipo', 'is_badge': True, 'badge_class': 'info'},
        {'field': 'get_estado_display', 'label': 'Estado', 'is_badge': True, 'badge_class': 'primary'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'nombre_contenedor', 'label': 'Nombre'},
        {'field': 'fk_lugar_general', 'label': 'Lugar'},
        {'field': 'fk_padre', 'label': 'Contenedor Padre'},
        {'field': 'get_tipo_contenedor_display', 'label': 'Tipo', 'is_badge': True},
        {'field': 'get_modo_almacenamiento_display', 'label': 'Modo'},
        {'field': 'get_estado_display', 'label': 'Estado', 'is_badge': True},
        {'field': 'capacidad_maxima', 'label': 'Capacidad Máxima'},
        {'field': 'observacion', 'label': 'Observaciones', 'full_width': True},
    ]

    def get_queryset(self):
        """Ordenar con select_related."""
        return self.model.objects.select_related(
            'fk_lugar_general', 'fk_padre'
        ).order_by('fk_lugar_general__nombre_lugar', 'nombre_contenedor')

    def get_initial_data(self, request):
        """Pre-llenar lugar si viene en URL."""
        lugar_id = request.GET.get('lugar')
        if lugar_id:
            return {'fk_lugar_general': lugar_id}
        return {}

    def can_delete(self, obj):
        """No permitir eliminar si tiene subcontenedores o obras."""
        num_subcontenedores = obj.subcontenedores.count()
        num_obras = obj.obras_actuales()
        reasons = []
        if num_subcontenedores > 0:
            reasons.append(f'{num_subcontenedores} subcontenedor(es)')
        if num_obras > 0:
            reasons.append(f'{num_obras} obra(s) almacenada(s)')
        return len(reasons) == 0, reasons

    def get_detail_sections(self, obj):
        """Mostrar subcontenedores y estadísticas."""
        sections = []

        # Subcontenedores
        subcontenedores = obj.subcontenedores.order_by('nombre_contenedor')
        sections.append({
            'title': 'Subcontenedores',
            'items': list(subcontenedores),
            'columns': [
                {'field': 'nombre_contenedor', 'label': 'Nombre'},
                {'field': 'get_tipo_contenedor_display', 'label': 'Tipo'},
                {'field': 'get_estado_display', 'label': 'Estado'},
            ],
            'empty_text': 'Este contenedor no tiene subcontenedores.',
            'action_url': 'contenedor:contenedor_detail',
            'action_label': 'Ver',
        })

        return sections


# Instancia para usar en urls.py
contenedor_views = ContenedorViews()

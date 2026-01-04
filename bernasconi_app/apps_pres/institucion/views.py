"""
CRUD de Instituciones usando el mixin genérico.
Este es el patrón recomendado para nuevos CRUDs.
"""

from apps.core.crud_views import CRUDViewMixin
from .models import Institucion
from .forms import InstitucionForm


class InstitucionViews(CRUDViewMixin):
    model = Institucion
    form_class = InstitucionForm
    app_name = 'institucion'

    # Búsqueda
    search_fields = ['nombre', 'direccion', 'contacto_persona', 'email']

    # Filtros
    filters = [
        {
            'name': 'tipo',
            'label': 'Tipo',
            'field': 'tipo_institucion',
            'choices': Institucion.TIPO_INSTITUCION_CHOICES,
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'nombre', 'label': 'Nombre', 'is_link': True},
        {'field': 'get_tipo_institucion_display', 'label': 'Tipo', 'is_badge': True, 'badge_class': 'primary'},
        {'field': 'contacto_persona', 'label': 'Contacto'},
        {'field': 'telefono', 'label': 'Teléfono'},
        {'field': 'email', 'label': 'Email'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'nombre', 'label': 'Nombre'},
        {'field': 'get_tipo_institucion_display', 'label': 'Tipo', 'is_badge': True},
        {'field': 'direccion', 'label': 'Dirección', 'full_width': True},
        {'field': 'contacto_persona', 'label': 'Persona de Contacto'},
        {'field': 'telefono', 'label': 'Teléfono'},
        {'field': 'email', 'label': 'Email'},
    ]

    def can_delete(self, obj):
        """Verificar si tiene préstamos o donaciones asociadas."""
        reasons = []
        num_prestamos_origen = obj.prestamos_origen.count()
        num_prestamos_destino = obj.prestamos_destino.count()
        num_donaciones = obj.donaciones_realizadas.count()

        if num_prestamos_origen > 0:
            reasons.append(f'{num_prestamos_origen} préstamo(s) como origen')
        if num_prestamos_destino > 0:
            reasons.append(f'{num_prestamos_destino} préstamo(s) como destino')
        if num_donaciones > 0:
            reasons.append(f'{num_donaciones} donación(es)')

        return len(reasons) == 0, reasons

    def get_detail_sections(self, obj):
        """Mostrar préstamos y donaciones relacionadas."""
        sections = []

        # Préstamos como origen
        prestamos_origen = obj.prestamos_origen.all()[:10]
        if prestamos_origen.exists() or True:  # Siempre mostrar sección
            sections.append({
                'title': 'Préstamos (como origen)',
                'items': list(prestamos_origen),
                'columns': [
                    {'field': 'n_de_prestamo', 'label': 'N° Préstamo'},
                    {'field': 'ficha', 'label': 'Obra'},
                    {'field': 'get_estado_display', 'label': 'Estado'},
                ],
                'empty_text': 'No hay préstamos como institución de origen.',
            })

        # Donaciones
        donaciones = obj.donaciones_realizadas.all()[:10]
        if donaciones.exists() or True:
            sections.append({
                'title': 'Donaciones realizadas',
                'items': list(donaciones),
                'columns': [
                    {'field': 'ficha', 'label': 'Obra'},
                    {'field': 'fecha_donacion', 'label': 'Fecha'},
                    {'field': 'get_condicion_legal_display', 'label': 'Condición'},
                ],
                'empty_text': 'No hay donaciones registradas.',
            })

        return sections


# Instancia para usar en urls.py
institucion_views = InstitucionViews()

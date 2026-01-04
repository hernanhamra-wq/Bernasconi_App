"""
Vistas del módulo core: Auditoría y configuración del sistema.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.apps import apps


@login_required
def auditoria_view(request):
    """
    Vista de auditoría: muestra los últimos cambios en el sistema.
    Solo lectura, sin capacidad de editar/eliminar.
    """
    # Modelos que heredan de AuditableModel y queremos auditar
    MODELOS_AUDITABLES = [
        ('ficha_tecnica', 'FichaTecnica', 'Ficha Técnica'),
        ('autor', 'Autor', 'Autor'),
        ('material', 'Material', 'Material'),
        ('investigacion', 'Investigacion', 'Investigación'),
        ('intervencion', 'Intervencion', 'Intervención'),
    ]

    # Filtros
    modelo_filtro = request.GET.get('modelo', '')
    usuario_filtro = request.GET.get('usuario', '')
    fecha_desde = request.GET.get('desde', '')
    fecha_hasta = request.GET.get('hasta', '')

    # Recopilar registros de todos los modelos auditables
    registros = []

    for app_label, model_name, display_name in MODELOS_AUDITABLES:
        try:
            Model = apps.get_model(app_label, model_name)

            # Verificar que tiene campos de auditoría
            if not hasattr(Model, 'updated_at'):
                continue

            # Si hay filtro de modelo, saltar los que no coinciden
            if modelo_filtro and modelo_filtro != app_label:
                continue

            queryset = Model.objects.all().select_related('created_by', 'updated_by')

            # Filtrar por usuario
            if usuario_filtro:
                queryset = queryset.filter(
                    Q(created_by_id=usuario_filtro) | Q(updated_by_id=usuario_filtro)
                )

            # Filtrar por fechas
            if fecha_desde:
                queryset = queryset.filter(updated_at__date__gte=fecha_desde)
            if fecha_hasta:
                queryset = queryset.filter(updated_at__date__lte=fecha_hasta)

            # Obtener últimos 100 de cada modelo
            for obj in queryset.order_by('-updated_at')[:100]:
                registros.append({
                    'modelo': display_name,
                    'app_label': app_label,
                    'objeto': str(obj),
                    'objeto_id': obj.pk,
                    'created_at': obj.created_at,
                    'created_by': obj.created_by,
                    'updated_at': obj.updated_at,
                    'updated_by': obj.updated_by,
                })
        except LookupError:
            continue

    # Ordenar por fecha de modificación descendente
    registros.sort(key=lambda x: x['updated_at'], reverse=True)

    # Paginar
    paginator = Paginator(registros, 50)
    page = request.GET.get('page', 1)
    registros_paginados = paginator.get_page(page)

    # Obtener lista de usuarios para el filtro
    from apps.usuarios.models import Usuario
    usuarios = Usuario.objects.filter(is_active=True).order_by('username')

    context = {
        'registros': registros_paginados,
        'total': len(registros),
        'modelos': MODELOS_AUDITABLES,
        'usuarios': usuarios,
        'filtros': {
            'modelo': modelo_filtro,
            'usuario': usuario_filtro,
            'desde': fecha_desde,
            'hasta': fecha_hasta,
        }
    }

    return render(request, 'core/auditoria.html', context)

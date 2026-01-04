"""
CRUD de Catálogo Multimedia.
- Vista global para gestión masiva
- Vistas por ficha para subir/gestionar desde el detalle de ficha
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.core.crud_views import CRUDViewMixin
from apps.ficha_tecnica.models import FichaTecnica
from .models import CatalogoMultimedia
from .forms import MultimediaForm, MultimediaFichaForm


# =============================================================================
# CRUD GLOBAL (desde menú principal)
# =============================================================================
class MultimediaViews(CRUDViewMixin):
    model = CatalogoMultimedia
    form_class = MultimediaForm
    app_name = 'multimedia'
    model_verbose = 'Multimedia'
    model_verbose_plural = 'Multimedia'
    page_bg_class = 'bg-fichas'

    # Búsqueda
    search_fields = ['descripcion', 'ficha__titulo', 'ficha__inventario']

    # Filtros
    filters = [
        {
            'name': 'tipo',
            'label': 'Tipo',
            'field': 'tipo',
            'choices': CatalogoMultimedia.TIPO_ARCHIVO
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'ficha', 'label': 'Ficha', 'is_link': True},
        {'field': 'tipo', 'label': 'Tipo'},
        {'field': 'descripcion', 'label': 'Descripción'},
        {'field': 'archivo', 'label': 'Archivo'},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'ficha', 'label': 'Ficha Técnica'},
        {'field': 'tipo', 'label': 'Tipo'},
        {'field': 'descripcion', 'label': 'Descripción'},
        {'field': 'archivo', 'label': 'Archivo'},
    ]

    def get_queryset(self):
        return self.model.objects.select_related('ficha').order_by('-id')


# Instancia para urls.py
multimedia_views = MultimediaViews()


# =============================================================================
# VISTAS POR FICHA (integradas en detalle de ficha)
# =============================================================================

@login_required
def ficha_multimedia_list(request, ficha_pk):
    """Lista multimedia de una ficha específica."""
    ficha = get_object_or_404(FichaTecnica, pk=ficha_pk)
    multimedia = ficha.catalogo_multimedia.all().order_by('-id')

    return render(request, 'catalogo_multimedia/ficha_multimedia_list.html', {
        'ficha': ficha,
        'multimedia': multimedia,
        'page_bg_class': 'bg-fichas',
    })


@login_required
def ficha_multimedia_add(request, ficha_pk):
    """Agregar multimedia a una ficha específica."""
    ficha = get_object_or_404(FichaTecnica, pk=ficha_pk)

    if request.method == 'POST':
        form = MultimediaFichaForm(request.POST, request.FILES)
        if form.is_valid():
            multimedia = form.save(commit=False)
            multimedia.ficha = ficha
            multimedia.save()
            messages.success(request, 'Archivo multimedia agregado correctamente.')
            return redirect('multimedia:ficha_multimedia_list', ficha_pk=ficha.pk)
    else:
        form = MultimediaFichaForm()

    return render(request, 'catalogo_multimedia/ficha_multimedia_form.html', {
        'form': form,
        'ficha': ficha,
        'page_title': f'Agregar Multimedia - {ficha.titulo or ficha.inventario}',
        'page_bg_class': 'bg-fichas',
    })


@login_required
def ficha_multimedia_delete(request, ficha_pk, pk):
    """Eliminar multimedia de una ficha."""
    ficha = get_object_or_404(FichaTecnica, pk=ficha_pk)
    multimedia = get_object_or_404(CatalogoMultimedia, pk=pk, ficha=ficha)

    if request.method == 'POST':
        multimedia.delete()
        messages.success(request, 'Archivo multimedia eliminado.')
        return redirect('multimedia:ficha_multimedia_list', ficha_pk=ficha.pk)

    return render(request, 'catalogo_multimedia/ficha_multimedia_delete.html', {
        'multimedia': multimedia,
        'ficha': ficha,
        'page_bg_class': 'bg-fichas',
    })

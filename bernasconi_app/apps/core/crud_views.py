"""
Mixins y clases base para vistas CRUD genéricas.

Uso:
    from apps.core.crud_views import CRUDViewMixin

    class AutorViews(CRUDViewMixin):
        model = Autor
        form_class = AutorForm
        app_name = 'autor'
        ...

    # En urls.py
    views = AutorViews()
    urlpatterns = [
        path('', views.list_view, name='autor_list'),
        ...
    ]
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from functools import wraps


def login_required_method(method):
    """Decorador para métodos de clase que requieren login."""
    @wraps(method)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        return method(self, request, *args, **kwargs)
    return wrapper


class CRUDViewMixin:
    """
    Mixin base para vistas CRUD genéricas.

    Atributos requeridos:
        model: Modelo Django
        form_class: Clase de formulario
        app_name: Nombre de la app para URLs (ej: 'autor')

    Atributos opcionales:
        model_verbose: Nombre singular (default: model._meta.verbose_name)
        model_verbose_plural: Nombre plural (default: model._meta.verbose_name_plural)
        list_columns: Lista de columnas para la lista
        search_fields: Campos para búsqueda
        page_size: Items por página (default: 25)
        page_bg_class: Clase CSS para fondo (default: 'bg-fichas')
    """

    model = None
    form_class = None
    app_name = None

    # Opcionales
    model_verbose = None
    model_verbose_plural = None
    list_columns = None
    detail_fields = None
    search_fields = None
    filters = None
    page_size = 25
    page_bg_class = 'bg-fichas'
    form_max_width = '600px'

    def get_model_verbose(self):
        return self.model_verbose or self.model._meta.verbose_name.title()

    def get_model_verbose_plural(self):
        return self.model_verbose_plural or self.model._meta.verbose_name_plural.title()

    def get_list_url(self):
        return f'{self.app_name}:{self.app_name}_list'

    def get_create_url(self):
        return f'{self.app_name}:{self.app_name}_create'

    def get_detail_url(self):
        return f'{self.app_name}:{self.app_name}_detail'

    def get_edit_url(self):
        return f'{self.app_name}:{self.app_name}_edit'

    def get_delete_url(self):
        return f'{self.app_name}:{self.app_name}_delete'

    def get_queryset(self):
        """Override para personalizar queryset base."""
        return self.model.objects.all()

    def get_search_queryset(self, queryset, query):
        """Aplica búsqueda al queryset."""
        if not query or not self.search_fields:
            return queryset

        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f'{field}__icontains': query})

        return queryset.filter(q_objects)

    def get_list_columns(self):
        """Retorna columnas para la lista."""
        if self.list_columns:
            return self.list_columns
        # Default: primer campo como link
        return [
            {'field': 'id', 'label': 'ID'},
            {'field': '__str__', 'label': 'Nombre', 'is_link': True},
        ]

    def get_detail_fields(self):
        """Retorna campos para el detalle."""
        return self.detail_fields or []

    def get_detail_sections(self, obj):
        """Override para agregar secciones relacionadas al detalle."""
        return []

    def can_delete(self, obj):
        """
        Retorna (can_delete: bool, reasons: list).
        Override para validar si se puede eliminar.
        """
        return True, []

    def get_object_name(self, obj):
        """Retorna nombre para mostrar del objeto."""
        return str(obj)

    # ==================== VISTAS ====================

    @login_required_method
    def list_view(self, request):
        """Vista de lista."""
        query = request.GET.get('q', '').strip()

        queryset = self.get_queryset()

        if query:
            queryset = self.get_search_queryset(queryset, query)

        # Aplicar filtros
        has_filters = False
        active_filters = []
        if self.filters:
            for f in self.filters:
                value = request.GET.get(f['name'], '')
                if value:
                    has_filters = True
                    queryset = queryset.filter(**{f['field']: value})
                active_filters.append({
                    **f,
                    'current': value
                })

        paginator = Paginator(queryset, self.page_size)
        page = request.GET.get('page', 1)
        items = paginator.get_page(page)

        context = {
            'items': items,
            'query': query,
            'total': paginator.count,
            'has_filters': has_filters,
            'filters': active_filters,
            'show_search': bool(self.search_fields),
            'search_placeholder': f'Buscar {self.get_model_verbose().lower()}...',

            # URLs
            'list_url': self.get_list_url(),
            'create_url': self.get_create_url(),
            'detail_url': self.get_detail_url(),
            'edit_url': self.get_edit_url(),
            'delete_url': self.get_delete_url(),

            # Meta
            'model_verbose': self.get_model_verbose(),
            'model_verbose_plural': self.get_model_verbose_plural(),
            'columns': self.get_list_columns(),
            'page_bg_class': self.page_bg_class,
        }

        return render(request, 'crud/generic_list.html', context)

    @login_required_method
    def create_view(self, request):
        """Vista de creación."""
        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save()
                messages.success(
                    request,
                    f'{self.get_model_verbose()} "{obj}" creado correctamente.'
                )
                return redirect(self.get_list_url())
        else:
            initial = self.get_initial_data(request)
            form = self.form_class(initial=initial)

        context = {
            'form': form,
            'page_title': f'Nuevo {self.get_model_verbose()}',
            'submit_label': f'Crear {self.get_model_verbose()}',
            'cancel_url': self.get_list_url(),
            'page_bg_class': self.page_bg_class,
            'form_max_width': self.form_max_width,
        }

        return render(request, 'crud/generic_form.html', context)

    def get_initial_data(self, request):
        """Override para datos iniciales del formulario."""
        return {}

    @login_required_method
    def edit_view(self, request, pk):
        """Vista de edición."""
        obj = get_object_or_404(self.model, pk=pk)

        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    f'{self.get_model_verbose()} "{obj}" actualizado correctamente.'
                )
                return redirect(self.get_list_url())
        else:
            form = self.form_class(instance=obj)

        context = {
            'form': form,
            'object': obj,
            'page_title': f'Editar: {obj}',
            'submit_label': 'Guardar Cambios',
            'cancel_url': self.get_list_url(),
            'page_bg_class': self.page_bg_class,
            'form_max_width': self.form_max_width,
        }

        return render(request, 'crud/generic_form.html', context)

    @login_required_method
    def detail_view(self, request, pk):
        """Vista de detalle."""
        obj = get_object_or_404(self.model, pk=pk)

        context = {
            'object': obj,
            'page_title': str(obj),
            'fields': self.get_detail_fields(),
            'sections': self.get_detail_sections(obj),
            'list_url': self.get_list_url(),
            'edit_url': self.get_edit_url(),
            'page_bg_class': self.page_bg_class,
        }

        return render(request, 'crud/generic_detail.html', context)

    @login_required_method
    def delete_view(self, request, pk):
        """Vista de eliminación."""
        obj = get_object_or_404(self.model, pk=pk)

        can_delete, reasons = self.can_delete(obj)

        if request.method == 'POST':
            if can_delete:
                name = str(obj)
                obj.delete()
                messages.success(
                    request,
                    f'{self.get_model_verbose()} "{name}" eliminado correctamente.'
                )
            else:
                messages.error(
                    request,
                    f'No se puede eliminar "{obj}" porque está en uso.'
                )
            return redirect(self.get_list_url())

        context = {
            'object': obj,
            'object_name': self.get_object_name(obj),
            'model_verbose': self.get_model_verbose(),
            'can_delete': can_delete,
            'delete_reasons': reasons,
            'cancel_url': self.get_list_url(),
            'page_bg_class': self.page_bg_class,
        }

        return render(request, 'crud/generic_delete.html', context)

    def get_urls(self):
        """
        Retorna urlpatterns para incluir en urls.py.

        Uso:
            views = MiViews()
            urlpatterns = views.get_urls()
        """
        from django.urls import path

        return [
            path('', self.list_view, name=f'{self.app_name}_list'),
            path('nuevo/', self.create_view, name=f'{self.app_name}_create'),
            path('<int:pk>/', self.detail_view, name=f'{self.app_name}_detail'),
            path('<int:pk>/editar/', self.edit_view, name=f'{self.app_name}_edit'),
            path('<int:pk>/eliminar/', self.delete_view, name=f'{self.app_name}_delete'),
        ]

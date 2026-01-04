"""
CRUD de Usuarios usando el mixin genérico.
Nota: Usuarios tiene lógica especial (crear vs editar usa formularios diferentes).
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from apps.core.crud_views import CRUDViewMixin, login_required_method
from .models import Usuario
from .forms import UsuarioCreateForm, UsuarioEditForm


class UsuarioViews(CRUDViewMixin):
    model = Usuario
    form_class = UsuarioCreateForm  # Para crear
    app_name = 'usuario'
    model_verbose = 'Usuario'
    model_verbose_plural = 'Usuarios'

    # Búsqueda
    search_fields = ['username', 'email', 'first_name', 'last_name']

    # Filtros
    filters = [
        {
            'name': 'role',
            'label': 'Rol',
            'field': 'role',
            'choices': Usuario.ROLE_CHOICES,
        },
        {
            'name': 'activo',
            'label': 'Estado',
            'field': 'is_active',
            'choices': [(True, 'Activo'), (False, 'Inactivo')],
        }
    ]

    # Columnas de la lista
    list_columns = [
        {'field': 'username', 'label': 'Usuario', 'is_link': True},
        {'field': 'get_full_name', 'label': 'Nombre Completo'},
        {'field': 'email', 'label': 'Email'},
        {'field': 'get_role_display', 'label': 'Rol', 'is_badge': True, 'badge_class': 'info'},
        {'field': 'is_active', 'label': 'Activo', 'is_boolean': True},
    ]

    # Campos del detalle
    detail_fields = [
        {'field': 'id', 'label': 'ID'},
        {'field': 'username', 'label': 'Usuario'},
        {'field': 'get_full_name', 'label': 'Nombre Completo'},
        {'field': 'email', 'label': 'Email'},
        {'field': 'get_role_display', 'label': 'Rol', 'is_badge': True},
        {'field': 'telefono', 'label': 'Teléfono'},
        {'field': 'fecha_nacimiento', 'label': 'Fecha Nacimiento'},
        {'field': 'is_active', 'label': 'Activo'},
        {'field': 'date_joined', 'label': 'Fecha Registro'},
        {'field': 'last_login', 'label': 'Último Acceso'},
    ]

    def can_delete(self, obj):
        """No permitir eliminar si tiene registros creados."""
        reasons = []

        # Verificar registros creados por este usuario
        from apps.ficha_tecnica.models import FichaTecnica
        num_fichas = FichaTecnica.objects.filter(created_by=obj).count()

        if num_fichas > 0:
            reasons.append(f'{num_fichas} ficha(s) técnica(s) creadas')

        # No permitir eliminar el propio usuario
        # (esto se valida en la vista)

        return len(reasons) == 0, reasons

    @login_required_method
    def edit_view(self, request, pk):
        """Edición usa formulario diferente (sin contraseña)."""
        obj = get_object_or_404(self.model, pk=pk)

        if request.method == 'POST':
            form = UsuarioEditForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    f'Usuario "{obj.username}" actualizado correctamente.'
                )
                return redirect(self.get_list_url())
        else:
            form = UsuarioEditForm(instance=obj)

        context = {
            'form': form,
            'object': obj,
            'page_title': f'Editar: {obj.username}',
            'submit_label': 'Guardar Cambios',
            'cancel_url': self.get_list_url(),
            'page_bg_class': self.page_bg_class,
            'form_max_width': self.form_max_width,
        }

        return render(request, 'crud/generic_form.html', context)

    @login_required_method
    def delete_view(self, request, pk):
        """No permitir que un usuario se elimine a sí mismo."""
        obj = get_object_or_404(self.model, pk=pk)

        # Verificar que no se elimine a sí mismo
        if obj == request.user:
            messages.error(request, 'No puedes eliminar tu propio usuario.')
            return redirect(self.get_list_url())

        can_delete, reasons = self.can_delete(obj)

        if request.method == 'POST':
            if can_delete:
                name = str(obj)
                obj.delete()
                messages.success(
                    request,
                    f'Usuario "{name}" eliminado correctamente.'
                )
            else:
                messages.error(
                    request,
                    f'No se puede eliminar "{obj}" porque está en uso.'
                )
            return redirect(self.get_list_url())

        context = {
            'object': obj,
            'object_name': obj.username,
            'model_verbose': self.get_model_verbose(),
            'can_delete': can_delete,
            'delete_reasons': reasons,
            'cancel_url': self.get_list_url(),
            'page_bg_class': self.page_bg_class,
        }

        return render(request, 'crud/generic_delete.html', context)


# Instancia para usar en urls.py
usuario_views = UsuarioViews()

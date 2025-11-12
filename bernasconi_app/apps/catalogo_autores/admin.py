from django.contrib import admin
from .models import Autor, Obra, Colaboracion, Prestamo
from django.utils.html import format_html

# ===================================================================
# 1. ADMIN INLINE (Para gestionar Colaboraciones dentro del formulario Obra)
# ===================================================================

class ColaboracionInline(admin.TabularInline):
    """Permite añadir/editar Colaboraciones (Autores) directamente en la página de Obra."""
    model = Colaboracion
    extra = 1  # Muestra un campo vacío para añadir un nuevo colaborador
    autocomplete_fields = ['autor']  # Sugerencias automáticas al escribir

# ===================================================================
# 2. ADMIN MODELO AUTOR
# ===================================================================

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'nacionalidad', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'nacionalidad')
    list_filter = ('nacionalidad',)

# ===================================================================
# 3. ADMIN MODELO OBRA (Central)
# ===================================================================

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    """Gestión de obras en el panel de administración."""
    
    # Campos visibles en el listado de obras
    list_display = ('titulo', 'tipo_obra', 'display_autores', 'fecha_publicacion')

    # Filtros y búsquedas
    list_filter = ('tipo_obra', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion')

    # Estructura del formulario de edición
    fieldsets = (
        (None, {
            'fields': ('titulo', 'tipo_obra', 'descripcion')
        }),
        ('Información de Publicación', {
            'fields': ('fecha_publicacion',),
            'classes': ('collapse',)  # Se puede plegar
        }),
    )

    # ❌ Eliminado el filter_horizontal (no permitido si hay tabla intermedia)
    # filter_horizontal = ('autores',)

    # ✅ Se usa el inline para manejar autores a través de Colaboracion
    inlines = [ColaboracionInline]

    # Mostrar los autores asociados en la lista
    def display_autores(self, obj):
        autores = obj.autores.all()
        if not autores:
            return format_html('<i>Sin autores asignados</i>')
        nombres = [f"{a.nombre} {a.apellido}" for a in autores]
        return format_html('<br>'.join(nombres))

    display_autores.short_description = 'Autores'

# ===================================================================
# 4. ADMIN MODELO PRESTAMO
# ===================================================================

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    """Gestión de préstamos en el panel de administración."""
    
    list_display = ('obra', 'solicitante', 'fecha_prestamo', 'fecha_devolucion_estimada', 'devuelto')
    search_fields = ('obra__titulo', 'solicitante')
    list_filter = ('devuelto', 'fecha_prestamo')
    date_hierarchy = 'fecha_prestamo'
    actions = ['marcar_como_devuelto']

    # Acción personalizada para marcar préstamos como devueltos
    def marcar_como_devuelto(self, request, queryset):
        updated = queryset.update(devuelto=True)
        self.message_user(request, f"{updated} préstamos marcados como devueltos.")

    marcar_como_devuelto.short_description = "Marcar préstamos seleccionados como devueltos"

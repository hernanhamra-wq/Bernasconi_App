from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Autor,
    Obra,
    Colaboracion,
    Prestamo,
    MaterialTipo,
    Organizacion,
    Multimedia,
    Ubicacion
)

# ===================================================================
# INLINE PARA COLABORACIONES DENTRO DE OBRA
# ===================================================================
class ColaboracionInline(admin.TabularInline):
    model = Colaboracion
    extra = 1
    autocomplete_fields = ['autor']

# ===================================================================
# INLINE PARA MULTIMEDIA DENTRO DE OBRA
# ===================================================================
class MultimediaInline(admin.TabularInline):
    model = Multimedia
    extra = 1
    fields = ('url_foto', 'url_video', 'descripcion')
    readonly_fields = ()
    show_change_link = True

# ===================================================================
# ADMIN MODELO AUTOR
# ===================================================================
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'nacionalidad', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'nacionalidad')
    list_filter = ('nacionalidad',)

# ===================================================================
# ADMIN MODELO OBRA
# ===================================================================
@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_obra', 'display_autores', 'fecha_publicacion')
    list_filter = ('tipo_obra', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion')
    fieldsets = (
        (None, {'fields': ('titulo', 'tipo_obra', 'descripcion')}),
        ('Información de Publicación', {'fields': ('fecha_publicacion',), 'classes': ('collapse',)}),
    )
    inlines = [ColaboracionInline, MultimediaInline]

    def display_autores(self, obj):
        autores = obj.autores.all()
        if not autores:
            return format_html('<i>Sin autores asignados</i>')
        nombres = [f"{a.nombre} {a.apellido}" for a in autores]
        return format_html('<br>'.join(nombres))
    display_autores.short_description = 'Autores'

# ===================================================================
# ADMIN MODELO PRESTAMO
# ===================================================================
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('fk_item', 'solicitante', 'fecha_inicio', 'fecha_devolucion_estimada', 'devuelto')
    search_fields = ('fk_item__titulo', 'solicitante')
    list_filter = ('devuelto', 'fecha_inicio')
    date_hierarchy = 'fecha_inicio'
    actions = ['marcar_como_devuelto']

    def marcar_como_devuelto(self, request, queryset):
        updated = queryset.update(devuelto=True)
        self.message_user(request, f"{updated} préstamos marcados como devueltos.")
    marcar_como_devuelto.short_description = "Marcar préstamos seleccionados como devueltos"

# ===================================================================
# ADMIN MODELO MATERIALTIPO
# ===================================================================
@admin.register(MaterialTipo)
class MaterialTipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

# ===================================================================
# ADMIN MODELO ORGANIZACION
# ===================================================================
@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'contacto', 'telefono', 'email')
    search_fields = ('nombre', 'contacto', 'email')

# ===================================================================
# ADMIN MODELO MULTIMEDIA (registro independiente)
# ===================================================================
@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('fk_obra', 'url_foto', 'url_video', 'descripcion')
    search_fields = ('fk_obra__titulo', 'descripcion')
    list_filter = ('fk_obra',)

# ===================================================================
# ADMIN MODELO UBICACION
# ===================================================================
@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('sector', 'sala', 'caja')
    search_fields = ('sector', 'sala', 'caja')

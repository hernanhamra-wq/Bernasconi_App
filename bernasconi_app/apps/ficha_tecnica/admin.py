from django.contrib import admin
from .models import FichaTecnica
from apps.autor.models import FichaAutor
from apps.material.models import FichaTecnicaMaterial

# --- INLINES ---

class AutorInline(admin.TabularInline):
    model = FichaAutor
    extra = 1
    # Basado en tu modelo de Autor, si el campo es ForeignKey(Autor), usa 'autor'
    # Si te da error E037 aquí, cámbialo a 'fk_autor'
    autocomplete_fields = ['fk_autor'] 
    verbose_name = "Autor"
    verbose_name_plural = "Autores"

class MaterialInline(admin.TabularInline):
    model = FichaTecnicaMaterial
    extra = 1
    # ✅ CORRECCIÓN SEGÚN TU MODELO: El campo se llama 'material'
    autocomplete_fields = ['material'] 
    verbose_name = "Material / Técnica"
    verbose_name_plural = "Materiales / Técnicas"

# --- ADMIN PRINCIPAL ---

@admin.register(FichaTecnica)
class FichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'n_de_ficha', 'titulo', 'anio', 'fk_estado_funcional', 'estado_conservacion')
    search_fields = ('titulo', 'n_de_ficha', 'fk_estado_funcional__nombre') 
    list_filter = ('estado_conservacion', 'fk_estado_funcional', 'tipo_ejemplar', 'seguimiento')

    inlines = [AutorInline, MaterialInline]

    autocomplete_fields = (
        'fk_estado_funcional', 
        'fk_responsable_carga', 
        'fk_multimedia_principal',
        'fk_taller'
    )
    
    fieldsets = (
        ('Identificación / Inventario', {'fields': ('n_de_ficha', 'inventario', 'n_de_inventario_anterior')}),
        ('Descripción General', {'fields': ('titulo', 'descripcion', 'anio', 'observacion')}),
        ('Estado y Conservación', {'fields': ('estado_conservacion', 'fk_estado_funcional', 'seguimiento')}),
        ('Ejemplar y Taller', {'fields': ('tipo_ejemplar', 'edicion', 'series_legacy', 'fk_taller')}),
        ('Dimensiones', {'fields': ('dimensiones', ('ancho', 'alto', 'profundidad', 'diametro'))}),
        ('Relaciones y Multimedia', {'fields': ('fk_responsable_carga', 'fk_multimedia_principal')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'fk_estado_funcional', 'fk_taller', 'fk_responsable_carga', 'fk_multimedia_principal'
        )
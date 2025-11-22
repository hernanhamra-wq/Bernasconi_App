from django.contrib import admin
from .models import FichaTecnica

@admin.register(FichaTecnica)
class FichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'anio', 'fk_estado')   # ✅ mostramos el estado en el listado
    search_fields = ('titulo', 'fk_estado__nombre_estado') # ✅ búsqueda por título y estado
    autocomplete_fields = ('fk_estado', 'fk_responsable_carga', 'fk_serie', 'fk_multimedia_principal')

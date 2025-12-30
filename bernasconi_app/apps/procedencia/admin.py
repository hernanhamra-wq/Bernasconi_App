from django.contrib import admin
from .models import Procedencia


@admin.register(Procedencia)
class ProcedenciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_procedencia', 'pais', 'fecha_adquisicion']
    list_filter = ['tipo_procedencia', 'pais']
    search_fields = ['nombre', 'documentacion', 'observaciones']
    date_hierarchy = 'fecha_adquisicion'
    ordering = ['nombre']

from django.contrib import admin
from .models import Intervencion

@admin.register(Intervencion)
class IntervencionAdmin(admin.ModelAdmin):
    list_display = (
        'intervencion_id',
        'ficha',
        'n_intervencion',
        'responsable',
        'fecha_inicio',
        'fecha_finalizacion',
    )

    list_filter = ('responsable', 'fecha_inicio', 'fecha_finalizacion')

    search_fields = ('ficha__titulo', 'diagnostico', 'procedimientos')

    autocomplete_fields = ('ficha', 'responsable')

    ordering = ('ficha', 'n_intervencion')

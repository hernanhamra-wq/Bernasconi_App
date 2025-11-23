from django.contrib import admin
from .models import SeguimientoXilofago

@admin.register(SeguimientoXilofago)
class SeguimientoXilofagoAdmin(admin.ModelAdmin):
    list_display = (
        'seguimiento_id',
        'registro_plaga',
        'fecha_seguimiento',
        'nueva_actividad',
    )
    list_filter = (
        'nueva_actividad',
        'fecha_seguimiento',
    )
    search_fields = (
        'seguimiento_id',
        'registro_plaga__registro_id',
        'observacion',
    )
    ordering = ('-fecha_seguimiento',)
    autocomplete_fields = ('registro_plaga',)

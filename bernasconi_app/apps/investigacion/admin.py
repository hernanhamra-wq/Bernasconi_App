from django.contrib import admin
from .models import Investigacion

@admin.register(Investigacion)
class InvestigacionAdmin(admin.ModelAdmin):
    list_display = (
        'investigacion_id',
        'ficha',
        'num_investigacion',
        'titulo_investigacion',
        'investigador',
        'anio_realizacion',
    )

    list_filter = ('anio_realizacion', 'investigador')

    search_fields = (
        'titulo_investigacion',
        'detalle_investigacion',
        'ficha__titulo',
        'investigador__username',
    )

    autocomplete_fields = ('ficha', 'investigador')

    ordering = ('ficha', 'num_investigacion')

from django.contrib import admin
from .models import Donacion

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ficha',
        'institucion_donante',
        'fecha_donacion',
        'valuacion',
        'usuario',
        'responsable',
    )
    list_filter = ('institucion_donante', 'fecha_donacion', 'responsable')
    search_fields = ('ficha__titulo', 'institucion_donante__nombre', 'responsable__username')
    autocomplete_fields = ('ficha', 'institucion_donante', 'usuario', 'responsable')

# contenedor_ubicacion/admin.py

from django.contrib import admin
from .models import ContenedorUbicacion

@admin.register(ContenedorUbicacion)
class ContenedorUbicacionAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_contenedor",
        "tipo_contenedor",
        "fk_lugar_general",
        "fk_padre",
        "estado",
        "capacidad_maxima",
    )
    list_filter = ("tipo_contenedor", "modo_almacenamiento", "estado", "fk_lugar_general")
    search_fields = ("nombre_contenedor", "observacion")
    autocomplete_fields = ("fk_padre", "fk_lugar_general")

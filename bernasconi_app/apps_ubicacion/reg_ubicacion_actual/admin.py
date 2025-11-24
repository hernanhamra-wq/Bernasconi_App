from django.contrib import admin
from .models import RegUbicacionActual


@admin.register(RegUbicacionActual)
class RegUbicacionActualAdmin(admin.ModelAdmin):
    list_display = (
        "fk_ficha",
        "fk_estado",
        "fk_lugar",
        "fk_contenedor",
        "fecha_desde",
    )

    list_filter = (
        "fk_estado",
        "fk_lugar",
        "fk_contenedor",
        "fecha_desde",
    )

    search_fields = (
        "fk_ficha__titulo",
        "fk_ficha__inventario",
        "fk_ficha__n_de_ficha",
        "fk_lugar__nombre_lugar",
        "fk_contenedor__nombre_contenedor",
    )

    autocomplete_fields = (
        "fk_ficha",
        "fk_estado",
        "fk_lugar",
        "fk_contenedor",
    )

    date_hierarchy = "fecha_desde"

    readonly_fields = ("fecha_desde",)

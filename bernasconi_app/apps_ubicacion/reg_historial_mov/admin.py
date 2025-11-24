from django.contrib import admin
from .models import RegHistorialMov


@admin.register(RegHistorialMov)
class RegHistorialMovAdmin(admin.ModelAdmin):
    list_display = (
        "fk_ficha",
        "fk_estado",
        "fk_lugar_destino",
        "fk_contenedor_destino",
        "fecha_movimiento",
        "fk_responsable_mov",
        "motivo",
    )

    list_filter = (
        "fk_estado",
        "fk_lugar_destino",
        "fk_contenedor_destino",
        "fk_responsable_mov",
        "fecha_movimiento",
    )

    search_fields = (
        "fk_ficha__titulo",
        "fk_ficha__inventario",
        "fk_ficha__n_de_ficha",
        "motivo",
    )

    autocomplete_fields = (
        "fk_ficha",
        "fk_estado",
        "fk_lugar_destino",
        "fk_contenedor_destino",
        "fk_responsable_mov",
    )

    date_hierarchy = "fecha_movimiento"

    readonly_fields = ("fecha_movimiento",)

    ordering = ("-fecha_movimiento",)

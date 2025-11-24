from django.contrib import admin
from .models import UbicacionLugar

@admin.register(UbicacionLugar)
class UbicacionLugarAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre_lugar",
        "tipo_lugar",
        "permite_contenedores",
    )
    list_filter = ("tipo_lugar", "permite_contenedores")
    search_fields = ("nombre_lugar",)
    ordering = ("nombre_lugar",)

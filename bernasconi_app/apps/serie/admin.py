from django.contrib import admin
from .models import Serie

@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "ficha", "original", "anio_impresion", "taller_reimpresion")
    list_filter = ("original", "anio_impresion")
    search_fields = ("nombre", "taller_reimpresion")
    ordering = ("nombre",)

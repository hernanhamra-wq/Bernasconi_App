from django.contrib import admin
from .models import ManejoPlagas

@admin.register(ManejoPlagas)
class ManejoPlagasAdmin(admin.ModelAdmin):
    list_display = ("id", "ficha", "tipo_plaga", "responsable", "titulo")
    list_filter = ("tipo_plaga", "responsable")
    search_fields = ("titulo", "propuesta_detalle", "ficha__titulo_obra")
    list_per_page = 20

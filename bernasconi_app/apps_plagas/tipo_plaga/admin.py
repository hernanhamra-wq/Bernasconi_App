from django.contrib import admin
from .models import TipoPlaga

@admin.register(TipoPlaga)
class TipoPlagaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre", "descripcion")
    list_per_page = 20

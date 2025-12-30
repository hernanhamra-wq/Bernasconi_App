from django.contrib import admin
from .models import CatalogoMultimedia

@admin.register(CatalogoMultimedia)
class CatalogoMultimediaAdmin(admin.ModelAdmin):
    list_display = ("id", "ficha", "tipo", "archivo", "descripcion")
    list_filter = ("tipo",)
    search_fields = ("archivo", "descripcion")
    ordering = ("ficha", "tipo")

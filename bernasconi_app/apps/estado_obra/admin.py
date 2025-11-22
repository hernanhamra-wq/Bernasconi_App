from django.contrib import admin
from .models import EstadoObra

@admin.register(EstadoObra)
class EstadoObraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_estado')   # ✅ muestra id y nombre
    search_fields = ('nombre_estado',)       # ✅ permite buscar por nombre

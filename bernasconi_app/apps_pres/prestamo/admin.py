from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        'n_de_prestamo',
        'ficha',
        'institucion_origen',
        'institucion_destino',
        'fecha_inicio',
        'fecha_fin_prevista',
        'fecha_devolucion_real',
    )

    list_filter = (
        'institucion_origen',
        'institucion_destino',
        'fecha_inicio',
        'fecha_fin_prevista',
    )

    search_fields = (
        'n_de_prestamo',
        'ficha__titulo',  # si FichaTecnica tiene título
    )
from django.contrib import admin

# Register your models here.

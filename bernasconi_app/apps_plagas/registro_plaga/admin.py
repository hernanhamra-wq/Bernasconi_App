from django.contrib import admin
from .models import RegistroPlaga


@admin.register(RegistroPlaga)
class RegistroPlagaAdmin(admin.ModelAdmin):
    list_display = (
        'registro_id',
        'ficha',
        'manejo',
        'fecha_registro',
        'tipologia_plaga',
    )
    list_filter = ('tipologia_plaga', 'fecha_registro')
    search_fields = ('registro_id', 'ficha__titulo')

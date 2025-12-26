from django.contrib import admin
from .models import Taller

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'contacto')
    # ESTO ES LO QUE SOLUCIONA EL ERROR E039:
    search_fields = ('nombre',)
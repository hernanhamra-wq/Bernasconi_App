from django.contrib import admin
from .models import Taller


@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'persona_contacto', 'email', 'telefono')
    search_fields = ('nombre', 'persona_contacto', 'email')
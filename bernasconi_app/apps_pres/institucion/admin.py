from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Institucion

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo_institucion", "contacto_persona", "telefono", "email")
    search_fields = ("nombre", "tipo_institucion", "contacto_persona", "email")
    list_filter = ("tipo_institucion",)

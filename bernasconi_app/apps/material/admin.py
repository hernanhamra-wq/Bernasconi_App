from django.contrib import admin
from .models import Material, FichaTecnicaMaterial

class FichaTecnicaMaterialInline(admin.TabularInline):
    model = FichaTecnicaMaterial
    extra = 1
    # Verifica en tu models.py si el campo se llama 'ficha' o 'fk_ficha'
    # Si sigue fallando, intenta cambiarlo aquí:
    autocomplete_fields = ['fk_ficha'] 

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',) # Esto permite que otros lo busquen
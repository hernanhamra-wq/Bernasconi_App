from django.contrib import admin
from django.apps import apps
from .models import Material  # ✅ correcto

class FichaTecnicaMaterialInline(admin.TabularInline):
    model = apps.get_model('material', 'FichaTecnicaMaterial')  # ✅ correcto, el modelo vive en la app 'material'
    extra = 1
    autocomplete_fields = ['ficha']
    verbose_name = "Uso en ficha técnica"
    verbose_name_plural = "Usos en fichas técnicas"

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    inlines = [FichaTecnicaMaterialInline]

try:
    admin.site.register(Material, MaterialAdmin)  # ✅ evita el AlreadyRegistered si otro módulo ya lo registró
except admin.sites.AlreadyRegistered:
    pass  # ✅ si ya estaba registrado, no falla

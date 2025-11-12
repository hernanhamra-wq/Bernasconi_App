from django.apps import AppConfig

class CatalogosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.catalogos'   
    label = 'catalogos'         # ✅ Nombre limpio lógico del módulo
    verbose_name = "Catálogos"  # ✅ Cómo se verá en el admin


from django.apps import AppConfig

class EstadoObraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.estado_obra'   # ✅ ruta completa de la app
    verbose_name = "Catálogo de Estados Funcionales"

from django.apps import AppConfig

class MaterialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.material'   # ✅ correcto, aquí no había error
    verbose_name = 'Material'
    label = 'material'

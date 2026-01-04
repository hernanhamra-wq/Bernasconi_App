from .views import material_views

app_name = 'material'
urlpatterns = material_views.get_urls()

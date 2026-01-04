from .views import institucion_views

app_name = 'institucion'
urlpatterns = institucion_views.get_urls()

from .views import contenedor_views

app_name = 'contenedor'
urlpatterns = contenedor_views.get_urls()

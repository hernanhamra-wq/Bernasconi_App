from .views import estado_obra_views

app_name = 'estado_obra'
urlpatterns = estado_obra_views.get_urls()

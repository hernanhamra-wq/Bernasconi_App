from .views import movimiento_views

app_name = 'movimiento'
urlpatterns = movimiento_views.get_urls()

from .views import donacion_views

app_name = 'donacion'
urlpatterns = donacion_views.get_urls()

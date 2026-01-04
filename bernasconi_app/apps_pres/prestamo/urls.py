from .views import prestamo_views

app_name = 'prestamo'
urlpatterns = prestamo_views.get_urls()

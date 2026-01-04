from .views import lugar_views

app_name = 'ubicacion'
urlpatterns = lugar_views.get_urls()

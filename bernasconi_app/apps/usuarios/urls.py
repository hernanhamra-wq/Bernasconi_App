from .views import usuario_views

app_name = 'usuario'
urlpatterns = usuario_views.get_urls()

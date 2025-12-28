from django.urls import path
from . import views
from .views import FichaTecnicaListView

app_name = "ficha_tecnica"

urlpatterns = [
    # 1) Listado
    path("", FichaTecnicaListView.as_view(), name="ficha_tecnica_list"),

    # 2) Cargar ficha técnica (URL más limpia que "ficha-tecnica/")
    path("cargar/", views.cargar_ficha_tecnica, name="ficha_tecnica"),

    # 3) Buscar
    path("buscar/", views.buscar_ficha_tecnica, name="buscar_ficha_tecnica"),

    # 4) Detalle y edición (van al final para no interferir con rutas fijas)
    path("<int:pk>/", views.detalle_ficha_tecnica, name="detalle_ficha_tecnica"),
    path("<int:pk>/editar/", views.editar_ficha_tecnica, name="editar_ficha_tecnica"),
]

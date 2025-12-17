from django.urls import path
from . import views

app_name = "investigacion"

urlpatterns = [
    path("cargar/", views.cargar_investigacion, name="cargar_investigacion"),
    path("buscar/", views.buscar_investigacion, name="buscar_investigacion"),
    path("<int:pk>/", views.detalle_investigacion, name="detalle_investigacion"),
]

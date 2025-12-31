from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = "investigacion"

urlpatterns = [
    path("", lambda request: redirect("investigacion:buscar_investigacion"), name="investigacion_index"),
    path("cargar/", views.cargar_investigacion, name="cargar_investigacion"),
    path("buscar/", views.buscar_investigacion, name="buscar_investigacion"),
    path("<int:pk>/", views.detalle_investigacion, name="detalle_investigacion"),
]

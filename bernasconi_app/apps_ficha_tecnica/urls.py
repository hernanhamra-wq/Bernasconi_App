from django.urls import path
from .views import cargar_ficha_tecnica

urlpatterns = [
    path('ficha-tecnica/', cargar_ficha_tecnica, name='cargar_ficha_tecnica'),
]



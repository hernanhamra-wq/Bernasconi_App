from django.urls import path, include
from . import views
from .views import FichaTecnicaListView

urlpatterns = [
    path('', FichaTecnicaListView.as_view(), name='ficha_tecnica_list'),
    path('ficha-tecnica/', views.cargar_ficha_tecnica, name='ficha_tecnica'),
]
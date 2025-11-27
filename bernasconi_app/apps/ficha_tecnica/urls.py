from django.urls import path, include
from .views import FichaTecnicaListView

urlpatterns = [
    path('', FichaTecnicaListView.as_view(), name='ficha_tecnica_list'),
]
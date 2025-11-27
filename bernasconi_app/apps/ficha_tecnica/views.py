from django.shortcuts import render
from django.views.generic import ListView
from .models import FichaTecnica

class FichaTecnicaListView(ListView):
    model = FichaTecnica
    template_name = 'fichatecnica_list.html'
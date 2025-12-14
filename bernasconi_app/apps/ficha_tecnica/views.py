from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import FichaTecnica
from .forms import FichaTecnicaForm


class FichaTecnicaListView(ListView):
    model = FichaTecnica
    template_name = 'fichatecnica_list.html'
    
def cargar_ficha_tecnica(request):
    if request.method == 'POST':
        form = FichaTecnicaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ficha_tecnica')
    else:
        form = FichaTecnicaForm()

    return render(
        request,
        'ficha_tecnica/formulario.html',
        {'form': form}
    )

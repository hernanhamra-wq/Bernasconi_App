from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.ficha_tecnica.models import FichaTecnica
from .forms import FichaTecnicaForm

from apps.autor.models import FichaAutor


@login_required
def cargar_ficha_tecnica(request):
    if request.method == "POST":
        form = FichaTecnicaForm(request.POST)

        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.fk_responsable_carga = request.user
            ficha.save()

            autores = form.cleaned_data.get('autores')
            if autores:
                for idx, autor in enumerate(autores, start=1):
                    FichaAutor.objects.create(
                        fk_ficha=ficha,
                        fk_autor=autor,
                        orden=idx
                    )

            return redirect('cargar_ficha_tecnica')

    else:
        form = FichaTecnicaForm()

    return render(
        request,
        'ficha_tecnica/formulario.html',
        {'form': form}
    )
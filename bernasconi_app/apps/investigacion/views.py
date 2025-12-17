from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import InvestigacionForm
from .models import Investigacion


def cargar_investigacion(request):
    if request.method == "POST":
        form = InvestigacionForm(request.POST)
        if form.is_valid():
            inv = form.save()
            messages.success(request, "✅ Investigación guardada correctamente en la base de datos.")
            return redirect("investigacion:detalle_investigacion", pk=inv.pk)
        else:
            messages.error(request, "⚠️ Hay errores en el formulario. Revisá los campos.")
    else:
        form = InvestigacionForm()

    return render(request, "investigacion/formulario.html", {"form": form})


def detalle_investigacion(request, pk):
    inv = get_object_or_404(Investigacion, pk=pk)
    return render(request, "investigacion/detalle_investigacion.html", {"inv": inv})

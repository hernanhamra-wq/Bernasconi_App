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


from django.db.models import Q
from django.core.paginator import Paginator

from .forms import InvestigacionSearchForm


def buscar_investigacion(request):
    form = InvestigacionSearchForm(request.GET or None)

    qs = (
        Investigacion.objects
        .select_related("ficha", "investigador")
        .order_by("-anio_realizacion", "-investigacion_id")
    )

    query = ""
    if form.is_valid():
        query = form.cleaned_data.get("q", "").strip()
        if query:
            qs = qs.filter(
                Q(num_investigacion__icontains=query) |
                Q(titulo_investigacion__icontains=query) |
                Q(detalle_investigacion__icontains=query) |
                Q(anio_realizacion__icontains=query) |
                Q(ficha__titulo__icontains=query) |
                Q(investigador__username__icontains=query) |
                Q(investigador__first_name__icontains=query) |
                Q(investigador__last_name__icontains=query)
            ).distinct()

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "investigacion/buscar_investigacion.html",
        {
            "form": form,
            "query": query,
            "page_obj": page_obj,
            "results": page_obj.object_list,
        }
    )

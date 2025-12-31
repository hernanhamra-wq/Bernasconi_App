from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.views.generic import ListView

from .models import FichaTecnica
from .forms import FichaTecnicaForm, FichaTecnicaSearchForm

from django.contrib import messages 


# =========================
# LISTADO
# =========================
class FichaTecnicaListView(ListView):
    model = FichaTecnica
    # ✅ IMPORTANTE: ahora busca el template dentro de /templates/ficha_tecnica/
    template_name = "ficha_tecnica/fichatecnica_list.html"
    context_object_name = "fichas"
    ordering = ["-fecha_de_carga", "-id"]


# =========================
# CARGA
# =========================
def cargar_ficha_tecnica(request):
    if request.method == "POST":
        form = FichaTecnicaForm(request.POST, request.FILES)
        if form.is_valid():
            ficha = form.save()
            messages.success(request, "✅ Ficha técnica guardada correctamente en la base de datos.")
            return redirect("ficha_tecnica:detalle_ficha_tecnica", pk=ficha.pk)
    else:
        form = FichaTecnicaForm()

    return render(request, "ficha_tecnica/formulario.html", {"form": form})


# =========================
# BÚSQUEDA GLOBAL
# =========================
TEXT_FIELDS = [
    "inventario",
    "n_de_inventario_anterior",
    "titulo",
    "descripcion",
    "observacion",
    "anio",
    "dimensiones",
]

NUM_FIELDS = [
    "id",
    "n_de_ficha",
    "ancho",
    "alto",
    "diametro",
    "profundidad",
]

FK_FIELDS = [
    "fk_estado_funcional",
    "fk_responsable_carga",
    "fk_multimedia_principal",
    "fk_taller",
    "fk_procedencia",
]

M2M_LOOKUPS = [
    "materiales__nombre__icontains",
    "materiales__descripcion__icontains",
    "materiales_relacion__detalle__icontains",  # through: FichaTecnicaMaterial.detalle
]


def _try_parse_number(q: str):
    q = (q or "").strip().replace(",", ".")
    if not q:
        return None
    try:
        if q.isdigit():
            return int(q)
        return Decimal(q)
    except (InvalidOperation, ValueError):
        return None


def _try_parse_date(q: str):
    q = (q or "").strip()
    if not q:
        return None

    d = parse_date(q)  # YYYY-MM-DD
    if d:
        return d

    try:
        return datetime.strptime(q, "%d/%m/%Y").date()
    except ValueError:
        return None


def _try_parse_bool(q: str):
    q = (q or "").strip().lower()
    if q in {"1", "true", "si", "sí", "yes"}:
        return True
    if q in {"0", "false", "no"}:
        return False
    return None


def _safe_add_related_lookups(model, fk_name: str, candidates):
    try:
        field = model._meta.get_field(fk_name)
        rel_model = field.related_model
        rel_fields = {f.name for f in rel_model._meta.get_fields() if hasattr(f, "name")}
        return [f"{fk_name}__{c}__icontains" for c in candidates if c in rel_fields]
    except Exception:
        return []


def build_search_q(query: str) -> Q:
    query = (query or "").strip()
    if not query:
        return Q()

    q_obj = Q()

    # Texto
    for f in TEXT_FIELDS:
        q_obj |= Q(**{f"{f}__icontains": query})

    # Numéricos
    num_val = _try_parse_number(query)
    if num_val is not None:
        for f in NUM_FIELDS:
            q_obj |= Q(**{f"{f}": num_val})

    # Fecha
    date_val = _try_parse_date(query)
    if date_val is not None:
        q_obj |= Q(fecha_de_carga__date=date_val)

    # Boolean
    bool_val = _try_parse_bool(query)
    if bool_val is not None:
        q_obj |= Q(seguimiento=bool_val)

    # FKs - responsable (User)
    for lookup in _safe_add_related_lookups(
        FichaTecnica, "fk_responsable_carga", ["username", "first_name", "last_name", "email"]
    ):
        q_obj |= Q(**{lookup: query})

    # FKs - estado funcional
    for lookup in _safe_add_related_lookups(
        FichaTecnica, "fk_estado_funcional", ["nombre", "descripcion", "estado"]
    ):
        q_obj |= Q(**{lookup: query})

    # FKs - taller
    for lookup in _safe_add_related_lookups(
        FichaTecnica, "fk_taller", ["nombre", "descripcion"]
    ):
        q_obj |= Q(**{lookup: query})

    # FKs - procedencia
    for lookup in _safe_add_related_lookups(
        FichaTecnica, "fk_procedencia", ["nombre", "descripcion", "tipo"]
    ):
        q_obj |= Q(**{lookup: query})

    # FKs - multimedia
    for lookup in _safe_add_related_lookups(
        FichaTecnica, "fk_multimedia_principal", ["titulo", "nombre", "descripcion"]
    ):
        q_obj |= Q(**{lookup: query})

    # IDs de FK si query es numérico
    if num_val is not None:
        try:
            num_int = int(num_val)
        except Exception:
            num_int = None

        if num_int is not None:
            for fk in FK_FIELDS:
                q_obj |= Q(**{f"{fk}_id": num_int})

    # ManyToMany materiales + detalle del through
    for lookup in M2M_LOOKUPS:
        q_obj |= Q(**{lookup: query})

    return q_obj


def buscar_ficha_tecnica(request):
    form = FichaTecnicaSearchForm(request.GET or None)
    qs = (
        FichaTecnica.objects.all()
        .select_related("fk_estado_funcional", "fk_responsable_carga", "fk_taller", "fk_multimedia_principal", "fk_procedencia")
        .prefetch_related("materiales", "materiales_relacion")
        .order_by("-fecha_de_carga", "-id")
    )

    query = ""
    if form.is_valid():
        query = form.cleaned_data.get("q") or ""
        if query.strip():
            qs = qs.filter(build_search_q(query)).distinct()

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "ficha_tecnica/buscar_ficha_tecnica.html", {
        "form": form,
        "query": query,
        "page_obj": page_obj,
        "results": page_obj.object_list,
    })


# =========================
# DETALLE
# =========================
def detalle_ficha_tecnica(request, pk):
    ficha = get_object_or_404(
        FichaTecnica.objects
        .select_related("fk_estado_funcional", "fk_responsable_carga", "fk_taller", "fk_multimedia_principal", "fk_procedencia")
        .prefetch_related("materiales", "materiales_relacion"),
        pk=pk
    )
    return render(request, "ficha_tecnica/detalle_ficha_tecnica.html", {"ficha": ficha})


# =========================
# EDITAR
# =========================
def editar_ficha_tecnica(request, pk):
    ficha = get_object_or_404(FichaTecnica, pk=pk)

    if request.method == "POST":
        form = FichaTecnicaForm(request.POST, request.FILES, instance=ficha)
        if form.is_valid():
            form.save()
            return redirect("ficha_tecnica:detalle_ficha_tecnica", pk=ficha.pk)
    else:
        form = FichaTecnicaForm(instance=ficha)

    return render(request, "ficha_tecnica/editar_ficha_tecnica.html", {
        "form": form,
        "ficha": ficha
    })

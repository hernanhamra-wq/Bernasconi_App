# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Xilófagos (Registros de Plaga)
=========================================
Migra los registros de xilófagos desde el CSV.
Crea RegistroPlaga vinculados a FichaTecnica.
Idempotente: no duplica registros existentes (basado en ficha + fecha).
"""
import os
import sys
import csv
import django
from datetime import datetime

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.ficha_tecnica.models import FichaTecnica
from apps_plagas.registro_plaga.models import RegistroPlaga
from apps_plagas.tipo_plaga.models import TipoPlaga

User = get_user_model()

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "resumen- xilofagos.csv")

# ============================================================
# HELPERS
# ============================================================

def parsear_entero(valor):
    """Parsea un valor a entero, retorna 0 si no es válido."""
    if not valor:
        return 0
    try:
        return int(float(str(valor).strip()))
    except (ValueError, TypeError):
        return 0


def parsear_fecha(valor):
    """Parsea una fecha del CSV."""
    if not valor:
        return None

    valor = str(valor).strip()

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(valor, fmt).date()
        except ValueError:
            continue

    return None


def limpiar_inventario(valor):
    """Limpia el número de inventario para búsqueda."""
    if not valor:
        return None

    valor = str(valor).strip()
    # Remover BOM y caracteres especiales
    valor = valor.replace('\ufeff', '').strip()

    if not valor:
        return None

    return valor


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Xilófagos (RegistroPlaga)")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    # Pre-cargar fichas existentes
    # Crear mapa por inventario y también por n_de_ficha
    fichas_por_inventario = {f.inventario: f for f in FichaTecnica.objects.all() if f.inventario}
    fichas_por_nficha = {str(f.n_de_ficha): f for f in FichaTecnica.objects.all() if f.n_de_ficha}

    print(f"  📋 {len(fichas_por_inventario)} fichas por inventario")
    print(f"  📋 {len(fichas_por_nficha)} fichas por n_de_ficha")

    # Obtener tipo de plaga por defecto (Carcoma o xilófago sin identificar)
    tipo_xilofago = TipoPlaga.objects.filter(nombre__icontains='carcoma').first()
    if not tipo_xilofago:
        tipo_xilofago = TipoPlaga.objects.filter(nombre__icontains='xilófago').first()

    # Usuario legacy para asignar
    usuario_legacy = User.objects.filter(username='sistema_legacy').first()

    creados = 0
    actualizados = 0
    fichas_no_encontradas = 0
    errores = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Normalizar headers (quitar BOM y caracteres especiales)
        fieldnames = reader.fieldnames
        header_inventario = None
        header_fecha = None

        for h in fieldnames:
            h_clean = h.replace('\ufeff', '').lower().strip()
            if 'inventario' in h_clean:
                header_inventario = h
            if 'fecha' in h_clean and 'finalizacion' in h_clean:
                header_fecha = h

        print(f"  📋 Header inventario: {header_inventario}")
        print(f"  📋 Header fecha: {header_fecha}")

        for i, fila in enumerate(reader, start=1):
            try:
                # Obtener número de inventario
                num_inventario = limpiar_inventario(fila.get(header_inventario))

                if not num_inventario:
                    continue

                # Buscar ficha por inventario o por n_de_ficha
                ficha = fichas_por_inventario.get(num_inventario)
                if not ficha:
                    ficha = fichas_por_nficha.get(num_inventario)

                if not ficha:
                    fichas_no_encontradas += 1
                    continue

                # Obtener fecha
                fecha = parsear_fecha(fila.get(header_fecha))
                if not fecha:
                    # Usar fecha actual si no hay
                    fecha = datetime.now().date()

                # Obtener conteos
                conteo_larvas = parsear_entero(fila.get('larvas'))
                conteo_esqueletos = parsear_entero(fila.get('esqueletos'))
                conteo_incisiones = parsear_entero(fila.get('inciciones'))  # Nota: typo en CSV
                conteo_tapones = parsear_entero(fila.get('tapones'))

                # Crear o actualizar registro
                registro, created = RegistroPlaga.objects.update_or_create(
                    ficha=ficha,
                    fecha_registro=fecha,
                    defaults={
                        'conteo_larvas': conteo_larvas,
                        'conteo_esqueletos': conteo_esqueletos,
                        'conteo_incisiones': conteo_incisiones,
                        'conteo_tapones': conteo_tapones if conteo_tapones else None,
                        'tipologia_plaga': tipo_xilofago,
                        'usuario_registro': usuario_legacy,
                        'observaciones': f"Migrado desde CSV (fila {i})"
                    }
                )

                if created:
                    creados += 1
                else:
                    actualizados += 1

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"  ⚠ Error en fila {i}: {e}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Registros creados: {creados}")
    print(f"  🔄 Registros actualizados: {actualizados}")
    print(f"  ❓ Fichas no encontradas: {fichas_no_encontradas}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total en BD: {RegistroPlaga.objects.count()}")


if __name__ == "__main__":
    run()

# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Investigaciones
==========================
Migra las investigaciones desde el CSV.
Idempotente: no duplica registros existentes (basado en num_investigacion).
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
from apps.investigacion.models import Investigacion

User = get_user_model()

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "investigacion.csv")

# ============================================================
# HELPERS
# ============================================================

def parsear_entero(valor):
    """Parsea un valor a entero."""
    if not valor:
        return None
    try:
        return int(float(str(valor).strip()))
    except (ValueError, TypeError):
        return None


def limpiar_texto(valor):
    """Limpia un valor de texto."""
    if not valor:
        return None

    texto = str(valor).strip()
    # Remover BOM
    texto = texto.replace('\ufeff', '')

    if texto.lower() in ['', 'nan', 'none', 'null']:
        return None

    return texto


def limpiar_inventario(valor):
    """Limpia el número de inventario para búsqueda."""
    if not valor:
        return None

    valor = str(valor).strip()
    valor = valor.replace('\ufeff', '').strip()

    if not valor:
        return None

    return valor


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Investigaciones")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    # Pre-cargar fichas existentes
    fichas_por_inventario = {f.inventario: f for f in FichaTecnica.objects.all() if f.inventario}
    fichas_por_nficha = {str(f.n_de_ficha): f for f in FichaTecnica.objects.all() if f.n_de_ficha}

    print(f"  📋 {len(fichas_por_inventario)} fichas por inventario")

    # Usuario legacy
    usuario_legacy = User.objects.filter(username='sistema_legacy').first()

    creados = 0
    actualizados = 0
    fichas_no_encontradas = 0
    errores = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Encontrar headers
        fieldnames = reader.fieldnames
        header_num_inv = None
        header_num_investigacion = None

        for h in fieldnames:
            h_clean = h.replace('\ufeff', '').lower().strip()
            if 'inventario' in h_clean:
                header_num_inv = h
            if 'investigaci' in h_clean and 'num' in h_clean:
                header_num_investigacion = h

        print(f"  📋 Header inventario: {header_num_inv}")
        print(f"  📋 Header num investigación: {header_num_investigacion}")

        for i, fila in enumerate(reader, start=1):
            try:
                # Obtener número de investigación
                num_investigacion = parsear_entero(fila.get(header_num_investigacion))
                if not num_investigacion:
                    continue

                # Obtener número de inventario
                num_inventario = limpiar_inventario(fila.get(header_num_inv))
                if not num_inventario:
                    continue

                # Buscar ficha
                ficha = fichas_por_inventario.get(num_inventario)
                if not ficha:
                    ficha = fichas_por_nficha.get(num_inventario)

                if not ficha:
                    fichas_no_encontradas += 1
                    continue

                # Obtener datos
                titulo = limpiar_texto(fila.get('titulo')) or f"Investigación {num_investigacion}"
                detalle = limpiar_texto(fila.get('Investigacion')) or ""

                # Año
                anio_raw = fila.get('año') or fila.get('a\xf1o')  # Manejar encoding
                anio = parsear_entero(anio_raw)
                if not anio:
                    anio = datetime.now().year

                # Crear o actualizar
                investigacion, created = Investigacion.objects.update_or_create(
                    num_investigacion=num_investigacion,
                    defaults={
                        'ficha': ficha,
                        'titulo_investigacion': titulo[:255],
                        'detalle_investigacion': detalle,
                        'anio_realizacion': anio,
                        'investigador': usuario_legacy,
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
    print(f"  🆕 Investigaciones creadas: {creados}")
    print(f"  🔄 Investigaciones actualizadas: {actualizados}")
    print(f"  ❓ Fichas no encontradas: {fichas_no_encontradas}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total en BD: {Investigacion.objects.count()}")


if __name__ == "__main__":
    run()

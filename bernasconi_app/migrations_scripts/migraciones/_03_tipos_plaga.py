# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Tipos de Plaga
=========================
Crea catálogo de tipos de plaga desde JSON.
Idempotente: no duplica tipos existentes.
"""
import os
import sys
import json
import django

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from apps_plagas.tipo_plaga.models import TipoPlaga

# ============================================================
# RUTAS
# ============================================================
JSON_PATH = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "tipos_plaga_canonicos.json")

# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Tipos de Plaga")

    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: No se encuentra el JSON en {JSON_PATH}")
        return

    with open(JSON_PATH, encoding="utf-8") as f:
        tipos = json.load(f)

    creados = 0
    existentes = 0

    for tipo in tipos:
        nombre = tipo.get("nombre")
        if not nombre:
            continue

        obj, created = TipoPlaga.objects.get_or_create(
            nombre=nombre,
            defaults={
                "descripcion": tipo.get("descripcion", ""),
                "recomendaciones_tratamiento": tipo.get("recomendaciones_tratamiento", ""),
            }
        )

        if created:
            creados += 1
            print(f"  ✓ Creado: {nombre}")
        else:
            existentes += 1
            print(f"  · Ya existe: {nombre}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Tipos creados: {creados}")
    print(f"  📌 Ya existentes: {existentes}")
    print(f"  📊 Total en BD: {TipoPlaga.objects.count()}")


if __name__ == "__main__":
    run()

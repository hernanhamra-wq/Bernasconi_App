# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Usuarios Seed
========================
Crea usuarios iniciales del sistema desde JSON.
Idempotente: no duplica usuarios existentes.
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

from django.contrib.auth import get_user_model

User = get_user_model()

# ============================================================
# RUTAS
# ============================================================
JSON_PATH = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "usuarios_seed.json")

# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Usuarios Seed")

    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: No se encuentra el JSON en {JSON_PATH}")
        return

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    usuarios = data.get("usuarios", [])
    creados = 0
    existentes = 0

    for u in usuarios:
        username = u.get("username")
        if not username:
            continue

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": u.get("email", ""),
                "first_name": u.get("first_name", ""),
                "last_name": u.get("last_name", ""),
                "is_staff": u.get("is_staff", False),
                "is_superuser": u.get("is_superuser", False),
            }
        )

        if created:
            # Establecer password solo en creación
            password = u.get("password", "Bernasconi2024!")
            user.set_password(password)
            user.save()
            creados += 1
            print(f"  ✓ Creado: {username}")
        else:
            existentes += 1
            print(f"  · Ya existe: {username}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Usuarios creados: {creados}")
    print(f"  📌 Ya existentes: {existentes}")


if __name__ == "__main__":
    run()

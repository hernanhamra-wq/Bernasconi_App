# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Ficha-Material (M2M)
===============================
Crea las relaciones M2M entre fichas técnicas y materiales.
Usa la misma lógica de tokenización que _01_materiales.py.
Idempotente: no duplica relaciones existentes.
"""
import os
import sys
import csv
import json
import re
import django
from difflib import SequenceMatcher

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from apps.material.models import Material, FichaTecnicaMaterial
from apps.ficha_tecnica.models import FichaTecnica

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")
JSON_PATH = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "materiales_canonicos.json")

# ============================================================
# HELPERS (copiados de _01_materiales.py)
# ============================================================

def normalize_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.strip()


def tokenize_material(text):
    """
    Tokenizador estricto: separa por símbolos, camelcase,
    elimina palabras cortas y cualquier palabra con números.
    """
    if not text:
        return []

    # 1. Separar CamelCase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # 2. Separar por símbolos y conectores
    text = re.sub(r'(?i)\s+y\s+|\s+con\s+|[\+\/\(\)\-\.\*\:\,]', ' ', text)

    palabras = text.split()

    exclusiones = {
        "de", "en", "el", "la", "con", "del", "sin", "id", "los", "las",
        "para", "por", "como", "son", "sobre", "esta", "donde", "tiene",
        "azul", "blanco", "negro", "negra", "rojo", "roja", "gris", "marron",
        "bordo", "rosado", "rosada", "plateado", "dorado",
        "alterado", "amuecada", "amigdaloide", "bandeado", "barnizada",
        "bañado", "bordado", "cocida", "cocido", "color", "cristalina",
        "depósito", "enchapado", "enlozado", "entelada", "esmaltada",
        "especular", "forrado", "galvanizada", "magnética", "pintado",
        "posible", "priori", "revestido", "usado", "variedades",
        "broche", "cable", "caja", "cinta", "clavos", "cobertor", "conector",
        "cuadro", "etiqueta", "hojas", "marco", "moneda", "tapa", "uniones"
    }

    resultado = []
    for p in palabras:
        if any(char.isdigit() for char in p):
            continue
        p_norm = normalize_text(p)
        if p_norm and p_norm not in exclusiones and len(p_norm) > 3:
            resultado.append(p_norm)

    return resultado


def to_camel_case(text):
    return "".join(word.capitalize() for word in text.split())


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Ficha-Material (M2M)")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    # Cargar catálogo de materiales canónicos
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, encoding="utf-8") as f:
            canonicos = json.load(f)
        canon_map = {normalize_text(m["nombre"]): m["nombre"] for m in canonicos}
    else:
        canon_map = {}

    print(f"  📚 Cargados {len(canon_map)} materiales canónicos")

    # Pre-cargar materiales y fichas existentes
    materiales_db = {m.nombre: m for m in Material.objects.all()}
    # También crear mapa por nombre normalizado
    materiales_db_norm = {normalize_text(m.nombre): m for m in Material.objects.all()}
    fichas_db = {f.inventario: f for f in FichaTecnica.objects.all() if f.inventario}

    print(f"  📋 {len(materiales_db)} materiales en BD")
    print(f"  📋 {len(fichas_db)} fichas en BD")

    relaciones_creadas = 0
    relaciones_existentes = 0
    fichas_sin_material = 0
    materiales_no_encontrados = set()
    errores = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for i, fila in enumerate(reader, start=1):
            try:
                inventario = fila.get("inventario", "").strip()
                celda_materiales = fila.get("materiales", "").strip()

                if not inventario:
                    continue

                ficha = fichas_db.get(inventario)
                if not ficha:
                    continue

                if not celda_materiales:
                    fichas_sin_material += 1
                    continue

                # Tokenizar materiales
                tokens = tokenize_material(celda_materiales)

                for token in tokens:
                    # 1. Buscar en canon_map para obtener nombre canónico
                    nombre_material = None
                    if token in canon_map:
                        nombre_material = canon_map[token]
                    else:
                        # 2. Buscar por similaridad
                        for canon_key, canon_nombre in canon_map.items():
                            if similarity(token, canon_key) >= 0.85:
                                nombre_material = canon_nombre
                                break

                    if not nombre_material:
                        # 3. Usar nombre en CamelCase
                        nombre_material = to_camel_case(token)

                    # Buscar material en BD
                    material = materiales_db.get(nombre_material)
                    if not material:
                        # Buscar por nombre normalizado
                        material = materiales_db_norm.get(normalize_text(nombre_material))

                    if not material:
                        materiales_no_encontrados.add(nombre_material)
                        continue

                    # Crear relación M2M
                    rel, created = FichaTecnicaMaterial.objects.get_or_create(
                        ficha=ficha,
                        material=material
                    )

                    if created:
                        relaciones_creadas += 1
                    else:
                        relaciones_existentes += 1

                # Progreso cada 1000 registros
                if i % 1000 == 0:
                    print(f"    ... procesadas {i} filas")

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"  ⚠ Error en fila {i}: {e}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Relaciones creadas: {relaciones_creadas}")
    print(f"  📌 Ya existentes: {relaciones_existentes}")
    print(f"  📭 Fichas sin material: {fichas_sin_material}")
    print(f"  ❌ Errores: {errores}")
    if materiales_no_encontrados:
        print(f"  ⚠ Materiales no encontrados en BD ({len(materiales_no_encontrados)}):")
        for m in sorted(list(materiales_no_encontrados)[:10]):
            print(f"      - {m}")
        if len(materiales_no_encontrados) > 10:
            print(f"      ... y {len(materiales_no_encontrados) - 10} más")
    print(f"  📊 Total relaciones en BD: {FichaTecnicaMaterial.objects.count()}")


if __name__ == "__main__":
    run()

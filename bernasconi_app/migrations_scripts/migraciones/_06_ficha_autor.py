# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Ficha-Autor (M2M)
============================
Crea las relaciones M2M entre fichas técnicas y autores.
Usa la misma lógica de normalización que _02_autores.py.
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

from apps.autor.models import Autor, FichaAutor
from apps.ficha_tecnica.models import FichaTecnica

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")
JSON_PATH = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "autores_canonicos.json")

# ============================================================
# HELPERS (copiados de _02_autores.py)
# ============================================================

def normalize_text(text):
    """Normaliza texto para comparación."""
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    return text


def similarity(a, b):
    """Calcula similaridad entre dos strings."""
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def to_title_case(text):
    """Convierte a Title Case respetando preposiciones."""
    if not text:
        return ""
    words = text.strip().split()
    result = []
    preposiciones = {'de', 'del', 'la', 'las', 'los', 'el', 'y', 'e'}
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in preposiciones:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return ' '.join(result)


def load_canonicos(json_path):
    """Carga el JSON de autores canónicos."""
    if not os.path.exists(json_path):
        return {}, set()

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    variantes_map = {}

    for autor in data.get("autores", []):
        nombre = autor.get("nombre")
        if not nombre:
            continue
        variantes_map[normalize_text(nombre)] = nombre
        for variante in autor.get("variantes", []):
            variantes_map[normalize_text(variante)] = nombre

    for inst in data.get("instituciones", []):
        nombre = inst.get("nombre")
        if not nombre:
            continue
        variantes_map[normalize_text(nombre)] = nombre
        for variante in inst.get("variantes", []):
            variantes_map[normalize_text(variante)] = nombre

    ignorar = set()
    for val in data.get("ignorar", {}).get("valores", []):
        ignorar.add(normalize_text(val))

    return variantes_map, ignorar


def extraer_autores_de_texto(texto, variantes_map, ignorar):
    """
    Extrae autores de un texto que puede contener múltiples autores.
    Retorna lista de nombres canónicos.
    """
    if not texto:
        return []

    texto_norm = normalize_text(texto)

    if texto_norm in ignorar or not texto_norm:
        return []

    if texto_norm in variantes_map:
        return [variantes_map[texto_norm]]

    autores_encontrados = []

    # Patrón "Idea: X / Taco: Y"
    if "idea" in texto_norm and "taco" in texto_norm:
        partes = re.split(r'\n|taco:', texto, flags=re.IGNORECASE)
        for parte in partes:
            parte = re.sub(r'^.*?:', '', parte).strip()
            if parte:
                parte_norm = normalize_text(parte)
                if parte_norm in variantes_map:
                    autores_encontrados.append(variantes_map[parte_norm])
                elif parte_norm not in ignorar:
                    for var_key, canonical in variantes_map.items():
                        if similarity(parte_norm, var_key) >= 0.85:
                            autores_encontrados.append(canonical)
                            break
                    else:
                        autores_encontrados.append(to_title_case(parte))

    if autores_encontrados:
        return list(set(autores_encontrados))

    # Patrón separado por comas
    if ',' in texto:
        partes = texto.split(',')
        for parte in partes:
            parte = parte.strip()
            parte_norm = normalize_text(parte)
            if parte_norm in ignorar or not parte_norm:
                continue
            if parte_norm in variantes_map:
                autores_encontrados.append(variantes_map[parte_norm])
            else:
                encontrado = False
                for var_key, canonical in variantes_map.items():
                    if similarity(parte_norm, var_key) >= 0.85:
                        autores_encontrados.append(canonical)
                        encontrado = True
                        break
                if not encontrado:
                    autores_encontrados.append(to_title_case(parte))

    if autores_encontrados:
        return list(set(autores_encontrados))

    # Caso simple: un solo autor
    for var_key, canonical in variantes_map.items():
        if similarity(texto_norm, var_key) >= 0.85:
            return [canonical]

    return [to_title_case(texto)]


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Ficha-Autor (M2M)")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    variantes_map, ignorar = load_canonicos(JSON_PATH)
    print(f"  📚 Cargadas {len(variantes_map)} variantes de autores")

    # Pre-cargar autores y fichas existentes
    autores_db = {a.nombre: a for a in Autor.objects.all()}
    fichas_db = {f.inventario: f for f in FichaTecnica.objects.all() if f.inventario}

    print(f"  📋 {len(autores_db)} autores en BD")
    print(f"  📋 {len(fichas_db)} fichas en BD")

    relaciones_creadas = 0
    relaciones_existentes = 0
    fichas_sin_autor = 0
    errores = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for i, fila in enumerate(reader, start=1):
            try:
                inventario = fila.get("inventario", "").strip()
                texto_autor = fila.get("autor", "").strip()

                if not inventario:
                    continue

                ficha = fichas_db.get(inventario)
                if not ficha:
                    continue

                if not texto_autor:
                    fichas_sin_autor += 1
                    continue

                # Extraer autores del texto
                nombres_autor = extraer_autores_de_texto(texto_autor, variantes_map, ignorar)

                for orden, nombre_autor in enumerate(nombres_autor, start=1):
                    autor = autores_db.get(nombre_autor)
                    if not autor:
                        # Crear autor si no existe
                        autor, _ = Autor.objects.get_or_create(nombre=nombre_autor)
                        autores_db[nombre_autor] = autor

                    # Crear relación M2M
                    rel, created = FichaAutor.objects.get_or_create(
                        fk_ficha=ficha,
                        fk_autor=autor,
                        defaults={'orden': orden}
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
    print(f"  📭 Fichas sin autor: {fichas_sin_autor}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total relaciones en BD: {FichaAutor.objects.count()}")


if __name__ == "__main__":
    run()

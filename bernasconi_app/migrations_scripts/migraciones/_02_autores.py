# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Autores
==================
Extrae autores únicos del CSV de fichas técnicas.
Normaliza variantes usando el JSON de autores canónicos.
Idempotente: no duplica autores existentes.
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

from apps.autor.models import Autor

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")
JSON_PATH = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "autores_canonicos.json")

# ============================================================
# HELPERS
# ============================================================

def normalize_text(text):
    """Normaliza texto para comparación."""
    if not text:
        return ""
    text = text.strip().lower()
    # Remover múltiples espacios
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
    """Carga el JSON de autores canónicos y construye mapa de variantes."""
    if not os.path.exists(json_path):
        return {}, {}, []

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Mapa: variante_normalizada -> autor_canonico
    variantes_map = {}
    biografias = {}

    for autor in data.get("autores", []):
        nombre = autor.get("nombre")
        if not nombre:
            continue

        biografias[nombre] = autor.get("biografia")
        variantes_map[normalize_text(nombre)] = nombre

        for variante in autor.get("variantes", []):
            variantes_map[normalize_text(variante)] = nombre

    # También incluir instituciones
    for inst in data.get("instituciones", []):
        nombre = inst.get("nombre")
        if not nombre:
            continue

        variantes_map[normalize_text(nombre)] = nombre
        for variante in inst.get("variantes", []):
            variantes_map[normalize_text(variante)] = nombre

    # Valores a ignorar
    ignorar = set()
    for val in data.get("ignorar", {}).get("valores", []):
        ignorar.add(normalize_text(val))

    return variantes_map, biografias, ignorar


def extraer_autores_de_texto(texto, variantes_map, ignorar):
    """
    Extrae autores de un texto que puede contener múltiples autores.
    Detecta patrones como:
    - "Idea: X / Taco: Y"
    - "X, Y, Z"
    - "X y Y"
    """
    if not texto:
        return []

    texto_norm = normalize_text(texto)

    # Ignorar valores vacíos o desconocidos
    if texto_norm in ignorar or not texto_norm:
        return []

    # Buscar match exacto primero
    if texto_norm in variantes_map:
        return [variantes_map[texto_norm]]

    autores_encontrados = []

    # Patrón "Idea: X / Taco: Y"
    if "idea" in texto_norm and "taco" in texto_norm:
        # Separar por líneas o "taco:"
        partes = re.split(r'\n|taco:', texto, flags=re.IGNORECASE)
        for parte in partes:
            # Limpiar "idea:", "idea original:", etc.
            parte = re.sub(r'^.*?:', '', parte).strip()
            if parte:
                parte_norm = normalize_text(parte)
                if parte_norm in variantes_map:
                    autores_encontrados.append(variantes_map[parte_norm])
                elif parte_norm not in ignorar:
                    # Buscar por similaridad
                    for var_key, canonical in variantes_map.items():
                        if similarity(parte_norm, var_key) >= 0.85:
                            autores_encontrados.append(canonical)
                            break
                    else:
                        # Nuevo autor
                        autores_encontrados.append(to_title_case(parte))

    # Si encontramos autores con el patrón, retornar
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
                # Buscar por similaridad
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
    # Buscar por similaridad
    for var_key, canonical in variantes_map.items():
        if similarity(texto_norm, var_key) >= 0.85:
            return [canonical]

    # Nuevo autor - normalizar a Title Case
    return [to_title_case(texto)]


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Autores")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    variantes_map, biografias, ignorar = load_canonicos(JSON_PATH)
    print(f"  📚 Cargadas {len(variantes_map)} variantes de autores canónicos")

    # Extraer todos los autores únicos del CSV
    autores_unicos = set()

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            texto_autor = fila.get("autor", "").strip()
            if texto_autor:
                autores = extraer_autores_de_texto(texto_autor, variantes_map, ignorar)
                autores_unicos.update(autores)

    print(f"  🔍 Encontrados {len(autores_unicos)} autores únicos en CSV")

    # Persistir en BD
    creados = 0
    existentes = 0

    for nombre_autor in sorted(autores_unicos):
        if not nombre_autor:
            continue

        biografia = biografias.get(nombre_autor)

        autor, created = Autor.objects.get_or_create(
            nombre=nombre_autor,
            defaults={
                "biografia": biografia or ""
            }
        )

        if created:
            creados += 1
        else:
            existentes += 1

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Autores creados: {creados}")
    print(f"  📌 Ya existentes: {existentes}")
    print(f"  📊 Total en BD: {Autor.objects.count()}")


if __name__ == "__main__":
    run()

# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Fichas Técnicas
==========================
Migra las fichas técnicas desde el CSV.
Idempotente: usa inventario como clave única.

NO migra relaciones M2M (autores, materiales) - eso va en scripts separados.
"""
import os
import sys
import csv
import json
import re
import django
from datetime import datetime
from decimal import Decimal, InvalidOperation

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.ficha_tecnica.models import FichaTecnica

User = get_user_model()

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")
JSON_USUARIOS = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "usuarios_seed.json")

# ============================================================
# HELPERS
# ============================================================

def cargar_mapa_usuarios():
    """
    Carga el mapa de variantes de usuario desde el JSON.
    Retorna dict: variante_normalizada -> username
    """
    if not os.path.exists(JSON_USUARIOS):
        return {}

    with open(JSON_USUARIOS, encoding="utf-8") as f:
        data = json.load(f)

    mapa = {}
    for u in data.get("usuarios", []):
        username = u.get("username")
        if not username:
            continue

        # El username mismo
        mapa[username.lower()] = username

        # Variantes del CSV
        for variante in u.get("variantes_csv", []):
            mapa[variante.lower()] = username

    return mapa


def normalizar_responsable(texto, mapa_usuarios):
    """Normaliza el nombre del responsable de carga."""
    if not texto or not texto.strip():
        # Sin dato en CSV → asignar a sistema_legacy
        return "sistema_legacy"

    texto_norm = texto.strip().lower()

    if texto_norm in mapa_usuarios:
        return mapa_usuarios[texto_norm]

    # Si no lo encontramos, usar sistema_legacy
    return "sistema_legacy"


def parsear_numero_ficha(valor):
    """Parsea el número de ficha a entero."""
    if not valor:
        return None
    try:
        return int(float(str(valor).strip()))
    except (ValueError, TypeError):
        return None


def parsear_decimal(valor):
    """Parsea un valor decimal."""
    if not valor:
        return None
    try:
        valor_str = str(valor).strip().replace(",", ".")
        if valor_str in ['', '0', '0.0']:
            return None
        return Decimal(valor_str)
    except (InvalidOperation, ValueError):
        return None


def parsear_fecha(valor):
    """Parsea una fecha del CSV."""
    if not valor:
        return None

    valor = str(valor).strip()

    # Intentar varios formatos
    formatos = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%y",
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(valor, fmt)
        except ValueError:
            continue

    return None


def normalizar_estado_conservacion(valor):
    """Normaliza el estado de conservación a choices válidos."""
    if not valor:
        return None

    valor_lower = str(valor).strip().lower()

    if 'buen' in valor_lower:
        return 'BUENO'
    elif 'regular' in valor_lower:
        return 'REGULAR'
    elif 'mal' in valor_lower:
        return 'MALO'

    return None


def normalizar_series(valor):
    """
    Normaliza el campo SERIES a tipo_ejemplar y/o edicion.
    Retorna tupla (tipo_ejemplar, edicion, series_legacy)
    """
    if not valor:
        return None, None, None

    valor_str = str(valor).strip()
    valor_lower = valor_str.lower()

    tipo_ejemplar = None
    edicion = None

    # Detectar tipo
    if 'original' in valor_lower:
        tipo_ejemplar = 'original'
    elif 'copia' in valor_lower:
        tipo_ejemplar = 'copia'
    elif 'serie' in valor_lower:
        # Buscar número de serie
        match = re.search(r'serie\s*(\d)', valor_lower)
        if match:
            num = match.group(1)
            if 1 <= int(num) <= 6:
                tipo_ejemplar = f'serie_{num}'

    # Detectar edición (ej: "3/50", "prueba de artista")
    match_edicion = re.search(r'(\d+\s*/\s*\d+)', valor_str)
    if match_edicion:
        edicion = match_edicion.group(1)
    elif 'prueba' in valor_lower or 'p.a.' in valor_lower:
        edicion = 'Prueba de artista'

    return tipo_ejemplar, edicion, valor_str


def limpiar_texto(valor):
    """Limpia un valor de texto."""
    if not valor:
        return None

    texto = str(valor).strip()
    if texto.lower() in ['', 'nan', 'none', 'null']:
        return None

    return texto


def get_csv_value(fila, key):
    """Obtiene valor del CSV, manejando BOM en headers."""
    # Intentar key directo
    valor = fila.get(key)
    if valor is not None:
        return valor

    # Intentar con BOM al inicio
    valor = fila.get('\ufeff' + key)
    if valor is not None:
        return valor

    # Buscar key que contenga el texto (ignorando BOM)
    for k, v in fila.items():
        if k.replace('\ufeff', '') == key:
            return v

    return None


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Fichas Técnicas")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    mapa_usuarios = cargar_mapa_usuarios()
    print(f"  📋 Cargadas {len(mapa_usuarios)} variantes de usuarios")

    # Pre-cargar usuarios existentes
    usuarios_db = {u.username: u for u in User.objects.all()}

    creados = 0
    actualizados = 0
    errores = 0
    sin_inventario = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for i, fila in enumerate(reader, start=1):
            try:
                # Inventario es clave única
                inventario = limpiar_texto(fila.get("inventario"))

                if not inventario:
                    sin_inventario += 1
                    continue

                # Preparar datos
                n_de_ficha = parsear_numero_ficha(fila.get("n de ficha"))
                titulo = limpiar_texto(fila.get("titulo"))
                descripcion = limpiar_texto(fila.get("descripción"))
                observacion = limpiar_texto(fila.get("observación"))
                anio = limpiar_texto(fila.get("año"))
                dimensiones = limpiar_texto(fila.get("dimenciones"))

                # Dimensiones numéricas
                ancho = parsear_decimal(fila.get("Ancho"))
                alto = parsear_decimal(fila.get("Alto"))
                profundidad = parsear_decimal(fila.get("Profundo"))
                diametro = parsear_decimal(fila.get("diámetro"))

                # Estado de conservación
                estado_conservacion = normalizar_estado_conservacion(
                    fila.get("Estado de conservación")
                )

                # Series/Ejemplar
                tipo_ejemplar, edicion, series_legacy = normalizar_series(
                    fila.get("SERIES")
                )

                # Inventario anterior
                n_inv_anterior = limpiar_texto(fila.get("n de inventario anterior"))

                # Seguimiento (boolean)
                seguimiento_raw = limpiar_texto(fila.get("seguimiento"))
                seguimiento = seguimiento_raw and seguimiento_raw.lower() in ['si', 'sí', 'yes', '1', 'true']

                # Responsable de carga (header puede tener BOM)
                responsable_username = normalizar_responsable(
                    get_csv_value(fila, "responsable de carga"),
                    mapa_usuarios
                )
                responsable_obj = usuarios_db.get(responsable_username)

                # Buscar o crear ficha
                ficha, created = FichaTecnica.objects.update_or_create(
                    inventario=inventario,
                    defaults={
                        'n_de_ficha': n_de_ficha,
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'observacion': observacion,
                        'anio': anio,
                        'dimensiones': dimensiones,
                        'ancho': float(ancho) if ancho else None,
                        'alto': float(alto) if alto else None,
                        'profundidad': float(profundidad) if profundidad else None,
                        'diametro': float(diametro) if diametro else None,
                        'estado_conservacion': estado_conservacion,
                        'tipo_ejemplar': tipo_ejemplar,
                        'edicion': edicion,
                        'series_legacy': series_legacy,
                        'n_de_inventario_anterior': n_inv_anterior,
                        'seguimiento': seguimiento,
                        'fk_responsable_carga': responsable_obj,
                    }
                )

                if created:
                    creados += 1
                else:
                    actualizados += 1

                # Progreso cada 1000 registros
                if i % 1000 == 0:
                    print(f"    ... procesadas {i} filas")

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"  ⚠ Error en fila {i}: {e}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Fichas creadas: {creados}")
    print(f"  🔄 Fichas actualizadas: {actualizados}")
    print(f"  ⚠ Sin inventario (omitidas): {sin_inventario}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total en BD: {FichaTecnica.objects.count()}")


if __name__ == "__main__":
    run()

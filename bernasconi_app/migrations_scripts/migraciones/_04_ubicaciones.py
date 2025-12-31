# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Ubicaciones
======================
Extrae ubicaciones únicas del CSV de fichas técnicas.
Crea UbicacionLugar y ContenedorUbicacion dinámicamente.
Idempotente: no duplica ubicaciones existentes.
"""
import os
import sys
import csv
import re
import django

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")

# ============================================================
# HELPERS
# ============================================================

def inferir_tipo_lugar(texto):
    """Infiere el tipo de lugar basándose en el texto."""
    texto_lower = texto.lower()

    if 'sala' in texto_lower:
        return 'SALA'
    elif 'restaura' in texto_lower or 'taller' in texto_lower:
        return 'TALLER'
    elif 'archivo' in texto_lower:
        return 'ARCHIVO'
    elif 'laboratorio' in texto_lower:
        return 'LABORATORIO'
    elif 'cuarentena' in texto_lower or 'fumiga' in texto_lower:
        return 'CUARENTENA'
    elif 'externo' in texto_lower or 'casco' in texto_lower:
        return 'EXTERNO'
    else:
        return 'DEPOSITO'


def inferir_tipo_contenedor(texto):
    """Infiere el tipo de contenedor basándose en el texto."""
    texto_lower = texto.lower()

    if 'caja' in texto_lower:
        return 'CAJA'
    elif 'sobre' in texto_lower:
        return 'SOBRE'
    elif 'vitrina' in texto_lower:
        return 'VITRINA'
    elif 'estante' in texto_lower:
        return 'ESTANTE'
    elif 'planero' in texto_lower:
        return 'PLANERO'
    elif 'tubo' in texto_lower:
        return 'TUBO'
    elif 'carpeta' in texto_lower:
        return 'CARPETA'
    elif 'rack' in texto_lower:
        return 'RACK'
    else:
        return 'OTRO'


def parsear_ubicacion(ubicacion_raw):
    """
    Parsea el texto de ubicación del CSV.
    Retorna dict con lugar y contenedor.

    Ejemplos:
        "CN - B 9" → lugar: "CN-B9", tipo: DEPOSITO
        "CAJA 425 - SECTOR Q" → lugar: "Sector Q", contenedor: "Caja 425"
        "sector 30A" → lugar: "Sector 30A"
        "sala6" → lugar: "Sala 6", tipo: SALA
    """
    if not ubicacion_raw:
        return None

    texto = ubicacion_raw.strip()

    # Ignorar valores no válidos
    if texto.lower() in ['desconocido', 'desaparecido', 'desaparecida', '']:
        return None

    resultado = {
        'lugar_nombre': None,
        'lugar_tipo': 'DEPOSITO',
        'contenedor_nombre': None,
        'contenedor_tipo': None,
    }

    # Patrón: "CAJA XXX - SECTOR Y"
    match_caja_sector = re.match(r'CAJA\s+(\d+)\s*[-–]\s*SECTOR\s+(\w+)', texto, re.IGNORECASE)
    if match_caja_sector:
        num_caja = match_caja_sector.group(1)
        sector = match_caja_sector.group(2).upper()
        resultado['lugar_nombre'] = f"Sector {sector}"
        resultado['lugar_tipo'] = 'DEPOSITO'
        resultado['contenedor_nombre'] = f"Caja {num_caja}"
        resultado['contenedor_tipo'] = 'CAJA'
        return resultado

    # Patrón: "SECTOR X - CAJA YYY"
    match_sector_caja = re.match(r'SECTOR\s+(\w+)\s*[-–]\s*CAJA\s+(\d+)', texto, re.IGNORECASE)
    if match_sector_caja:
        sector = match_sector_caja.group(1).upper()
        num_caja = match_sector_caja.group(2)
        resultado['lugar_nombre'] = f"Sector {sector}"
        resultado['lugar_tipo'] = 'DEPOSITO'
        resultado['contenedor_nombre'] = f"Caja {num_caja}"
        resultado['contenedor_tipo'] = 'CAJA'
        return resultado

    # Patrón: "sector XXX caja YYY"
    match_sector_caja2 = re.match(r'sector\s+(\w+)\s+caja\s+(\d+)', texto, re.IGNORECASE)
    if match_sector_caja2:
        sector = match_sector_caja2.group(1).upper()
        num_caja = match_sector_caja2.group(2)
        resultado['lugar_nombre'] = f"Sector {sector}"
        resultado['lugar_tipo'] = 'DEPOSITO'
        resultado['contenedor_nombre'] = f"Caja {num_caja}"
        resultado['contenedor_tipo'] = 'CAJA'
        return resultado

    # Patrón: "CN - X Y" o "CN-XY" (Ciencias Naturales)
    match_cn = re.match(r'CN\s*[-–]?\s*([A-Z])\s*(\d+)?', texto, re.IGNORECASE)
    if match_cn:
        letra = match_cn.group(1).upper()
        num = match_cn.group(2) or ""
        resultado['lugar_nombre'] = f"CN-{letra}{num}"
        resultado['lugar_tipo'] = 'DEPOSITO'
        return resultado

    # Patrón: "sala X" o "salaX"
    match_sala = re.match(r'sala\s*(\d+|[a-zA-Z\s]+)', texto, re.IGNORECASE)
    if match_sala:
        sala_id = match_sala.group(1).strip()
        resultado['lugar_nombre'] = f"Sala {sala_id}"
        resultado['lugar_tipo'] = 'SALA'
        return resultado

    # Patrón: "sector XXX"
    match_sector = re.match(r'sector\s+(.+)', texto, re.IGNORECASE)
    if match_sector:
        sector_id = match_sector.group(1).strip()
        resultado['lugar_nombre'] = f"Sector {sector_id}"
        resultado['lugar_tipo'] = inferir_tipo_lugar(sector_id)
        return resultado

    # Patrón: "SECTOR X"
    match_sector2 = re.match(r'SECTOR\s+(\w+)', texto, re.IGNORECASE)
    if match_sector2:
        sector_id = match_sector2.group(1).upper()
        resultado['lugar_nombre'] = f"Sector {sector_id}"
        resultado['lugar_tipo'] = 'DEPOSITO'
        return resultado

    # Casos especiales
    if 'restaura' in texto.lower():
        resultado['lugar_nombre'] = "Sala de Restauración"
        resultado['lugar_tipo'] = 'TALLER'
        return resultado

    if 'archivo' in texto.lower():
        resultado['lugar_nombre'] = "Archivo"
        resultado['lugar_tipo'] = 'ARCHIVO'
        return resultado

    if 'casco' in texto.lower():
        resultado['lugar_nombre'] = "Casco Histórico"
        resultado['lugar_tipo'] = 'EXTERNO'
        return resultado

    # Por defecto, usar el texto como nombre de lugar
    resultado['lugar_nombre'] = texto[:100]  # Limitar longitud
    resultado['lugar_tipo'] = inferir_tipo_lugar(texto)
    return resultado


def parsear_sector(sector_raw):
    """Parsea el sector del CSV."""
    if not sector_raw or sector_raw.strip() == "":
        return None

    sector = sector_raw.strip().upper()
    return f"Sector {sector}"


def parsear_sala(sala_raw):
    """Parsea la sala del CSV."""
    if not sala_raw or sala_raw.strip() == "":
        return None

    sala = sala_raw.strip()

    # Normalizar
    if sala.lower().startswith('sala'):
        return f"Sala {sala[4:].strip()}"
    elif sala.lower() == 'naturales':
        return "Sala Ciencias Naturales"
    elif sala.lower() == 'cincioni':
        return "Sala Cincioni"
    elif 'pasillo' in sala.lower():
        return sala.title()
    elif sala.lower() in ['desaparecido', 'préstamo', 'cove']:
        return None
    else:
        return f"Sala {sala}"


def parsear_caja(caja_raw, lugar_obj):
    """Parsea la caja del CSV."""
    if not caja_raw:
        return None

    # Limpiar valor
    caja_str = str(caja_raw).strip()

    # Ignorar valores vacíos o cero
    if caja_str in ['', '0', '0.0']:
        return None

    # Convertir a entero si es posible
    try:
        num_caja = int(float(caja_str))
        if num_caja == 0:
            return None
        return {
            'nombre': f"Caja {num_caja}",
            'tipo': 'CAJA',
            'lugar': lugar_obj
        }
    except ValueError:
        return {
            'nombre': f"Caja {caja_str}",
            'tipo': 'CAJA',
            'lugar': lugar_obj
        }


def parsear_sobre(sobre_raw, lugar_obj):
    """Parsea el sobre del CSV."""
    if not sobre_raw:
        return None

    sobre_str = str(sobre_raw).strip()

    if sobre_str in ['', '0', '0.0']:
        return None

    try:
        num_sobre = int(float(sobre_str))
        if num_sobre == 0:
            return None
        return {
            'nombre': f"Sobre {num_sobre}",
            'tipo': 'SOBRE',
            'lugar': lugar_obj
        }
    except ValueError:
        return {
            'nombre': f"Sobre {sobre_str}",
            'tipo': 'SOBRE',
            'lugar': lugar_obj
        }


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Ubicaciones")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    lugares_unicos = {}  # nombre -> tipo
    contenedores_unicos = set()  # (nombre, lugar_nombre)

    # Primera pasada: extraer ubicaciones únicas
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            # Columna "ubicación"
            ubicacion_raw = fila.get("ubicación", "").strip()
            if ubicacion_raw:
                parsed = parsear_ubicacion(ubicacion_raw)
                if parsed and parsed['lugar_nombre']:
                    lugares_unicos[parsed['lugar_nombre']] = parsed['lugar_tipo']
                    if parsed['contenedor_nombre']:
                        contenedores_unicos.add((parsed['contenedor_nombre'], parsed['lugar_nombre'], parsed['contenedor_tipo']))

            # Columna "sector"
            sector_raw = fila.get("sector", "").strip()
            sector_nombre = parsear_sector(sector_raw)
            if sector_nombre and sector_nombre not in lugares_unicos:
                lugares_unicos[sector_nombre] = 'DEPOSITO'

            # Columna "sala"
            sala_raw = fila.get("sala", "").strip()
            sala_nombre = parsear_sala(sala_raw)
            if sala_nombre and sala_nombre not in lugares_unicos:
                lugares_unicos[sala_nombre] = 'SALA'

    print(f"  🔍 Encontrados {len(lugares_unicos)} lugares únicos")
    print(f"  🔍 Encontrados {len(contenedores_unicos)} contenedores únicos")

    # Crear lugares
    lugares_creados = 0
    lugares_existentes = 0
    lugares_map = {}  # nombre -> objeto

    for nombre, tipo in sorted(lugares_unicos.items()):
        lugar, created = UbicacionLugar.objects.get_or_create(
            nombre_lugar=nombre,
            defaults={
                'tipo_lugar': tipo,
                'permite_contenedores': tipo in ['DEPOSITO', 'ARCHIVO', 'TALLER'],
            }
        )
        lugares_map[nombre] = lugar

        if created:
            lugares_creados += 1
        else:
            lugares_existentes += 1

    print(f"  ✓ Lugares: {lugares_creados} creados, {lugares_existentes} existentes")

    # Crear contenedores
    contenedores_creados = 0
    contenedores_existentes = 0

    for cont_nombre, lugar_nombre, cont_tipo in sorted(contenedores_unicos):
        lugar_obj = lugares_map.get(lugar_nombre)
        if not lugar_obj:
            continue

        contenedor, created = ContenedorUbicacion.objects.get_or_create(
            nombre_contenedor=cont_nombre,
            fk_lugar_general=lugar_obj,
            defaults={
                'tipo_contenedor': cont_tipo or 'OTRO',
                'modo_almacenamiento': 'EN_CONTENEDOR',
                'estado': 'DISPONIBLE',
            }
        )

        if created:
            contenedores_creados += 1
        else:
            contenedores_existentes += 1

    print(f"  ✓ Contenedores: {contenedores_creados} creados, {contenedores_existentes} existentes")

    # Segunda pasada: cajas y sobres de columnas específicas
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            # Determinar lugar para caja/sobre
            sector_raw = fila.get("sector", "").strip()
            sector_nombre = parsear_sector(sector_raw)
            lugar_obj = lugares_map.get(sector_nombre) if sector_nombre else None

            if not lugar_obj:
                # Usar sala como fallback
                sala_raw = fila.get("sala", "").strip()
                sala_nombre = parsear_sala(sala_raw)
                lugar_obj = lugares_map.get(sala_nombre) if sala_nombre else None

            if lugar_obj:
                # Columna "caja"
                caja_data = parsear_caja(fila.get("caja"), lugar_obj)
                if caja_data:
                    ContenedorUbicacion.objects.get_or_create(
                        nombre_contenedor=caja_data['nombre'],
                        fk_lugar_general=caja_data['lugar'],
                        defaults={
                            'tipo_contenedor': caja_data['tipo'],
                            'modo_almacenamiento': 'EN_CONTENEDOR',
                            'estado': 'DISPONIBLE',
                        }
                    )

                # Columna "sobre"
                sobre_data = parsear_sobre(fila.get("sobre"), lugar_obj)
                if sobre_data:
                    ContenedorUbicacion.objects.get_or_create(
                        nombre_contenedor=sobre_data['nombre'],
                        fk_lugar_general=sobre_data['lugar'],
                        defaults={
                            'tipo_contenedor': sobre_data['tipo'],
                            'modo_almacenamiento': 'EN_CONTENEDOR',
                            'estado': 'DISPONIBLE',
                        }
                    )

    print(f"\n✔ Proceso finalizado.")
    print(f"  📊 Total lugares en BD: {UbicacionLugar.objects.count()}")
    print(f"  📊 Total contenedores en BD: {ContenedorUbicacion.objects.count()}")


if __name__ == "__main__":
    run()
